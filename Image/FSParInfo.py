import pytsk3
import pyewf

from tabulate import tabulate
from EWFImgInfo import *
from FSFileInfo import *
from Utils.log import *


class FSParInfo():
    def __init__(self, partition_handle, volume_info, image_info, image):
        '''
        Partitie informatie en gegevens, waaronder alle bestanden
        :param partition_handle: Handle naar fsPar
        :param volume_info: referentie naar volume
        :param image_info: referentie naar parent image class
        :param image: referentie naar parent image class
        '''
        # Opslaan belangrijke parameters
        self.image = image
        self.partition_handle = partition_handle
        self.volume_info = volume_info
        self.image_info = image_info

        # Uitlezen en opslaan van belangrijke partitie informatie
        self.size = self.partition_handle.len
        self.desc = self.partition_handle.desc
        self.addr = self.partition_handle.addr
        self.len = self.partition_handle.len

        # Aanmaken bestand / folder array
        self.dirs = []
        self.files = []

        try:
            # Fileformat uitlezen d.m.v. pytsk3
            # Partitie wordt uitgelezen het begin
            # de start offset van de partitie X de cluster grote van de image
            self.fs_handle = pytsk3.FS_Info(
                self.image_info, offset=self.partition_handle.start * self.volume_info.info.block_size)
        except IOError:
            Logger("Unable to open Filesystem from " + self.desc)

        Logger("Succesfully Mounted FileSystem of " + self.desc)

        # Referentie naar hoofdmap opslaan
        self.root = self.fs_handle.open_dir(path="/")
        # Bestanden vanaf hoofdmap uitlezen (inclusief subfolders)
        self.recurse_files()

        # Printig some info..
        Logger("{} Dirs and {} Files located".format(
            str(len(self.dirs)), str(len(self.files))))

    def get_root(self):
        '''
        Verkrijgt de hoofdmap van de partitie
        :return: None
        '''
        self.root = self.fs_handle.open_dir(path="/")

    def recurse_dir(self, dir, parent):
        '''
        Uitlezen van alle betanden en mappen van partitie
        :param dir: fsObject van map
        :param parent: string met parent location
        :return: None
        '''
        # Toevoegen van directory's adres aan map array
        # Alle mappen in de map array worden niet meer verwerkt om oneindige loops te voorkomen
        self.dirs.append(dir.info.meta.addr)
        # Submap toevoegen aan path, zodat een volledig path naar bestand wordt gemaakt
        parent = parent + dir.info.name.name + '\\'
        # tsk3's bestands object omzetten naar een directory
        dir = dir.as_directory()
        # Loopen door files in directory
        for object in dir:
            try:
                # Filetype vergelijken met type van map
                if object.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                    # Alleen als die map nog niet is verwerkt
                    if object.info.meta.addr not in self.dirs:
                        # Als object een map is wordt deze functie opnieuw aangeroepen
                        # Om de bestanden en mappen van deze map ook uit te lezen
                        self.recurse_dir(object, parent)
                else:
                    # Mocht het bestand van het type file zijn
                    # Bestand als FSFileInfo initaliseren, en opslaan naar file array
                    self.files.append(FSFileInfo(object, parent))
            except AttributeError:
                Debugger('Error parsing Object: ' + object.info.name.name)

    def recurse_files(self):
        '''
        Eenmalige functie voor het uitlezen van alle files uit paritie
        :return: None
        '''
        # Root map toevoegen aan arraylist voor mappen
        # Deze map wordt in het vervolg niet meer verwerkt om oneindige loop's te voorkomen
        self.dirs.append(self.root.info.fs_file.meta.addr)
        # Mooie \\ toevoegen aan path
        parent = "\\"
        # Nested loop voor het uitlezen van mappen in mappen
        for object in self.root:
              # Filetype vergelijken met type van map
            try:
                  # Alleen als die map nog niet is verwerkt
                if object.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                    # Als object een map is wordt deze functie opnieuw aangeroepen
                    # Om de bestanden en mappen van deze map ook uit te lezen
                    self.recurse_dir(object, parent)
                else:
                    # Mocht het bestand van het type file zijn
                    # Bestand als FSFileInfo initaliseren, en opslaan naar file array
                    self.files.append(FSFileInfo(object, parent))
            except AttributeError:
                Debugger('Error parsing Object: ' + object.info.name.name)

    def files_rapport(self):
        '''
        Functie voor het maken van een file tabel
        Met alle files uitgleezen uit deze partitie
        :return: None
        '''
        # Aanmaken lege array
        attribute_array = []
        for object in self.files:
            # Laden van alle meta-data van ieder bestand in array
            attribute_array.append(object.get_attributes())

        # Printen van tabel
        print tabulate(attribute_array, headers=[
                       'Name', 'Size', 'Created', 'Changed', 'Modified', 'MD5', 'SHA256'])
