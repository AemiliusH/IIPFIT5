import pytsk3
import pyewf

from FSParInfo import *
from Utils.log import *


class EWFImgInfo(pytsk3.Img_Info):
    # Partitie array initialiseren
    partities = []

    def __init__(self, ewf_handle, image):
        # Opslaan belangrijke variable
        self.image = image
        self.ewf_handle = ewf_handle

        # Aanroepen van pytsk3.Img_info class, deze laad de image naar pytsk3
        super(EWFImgInfo, self).__init__(
            url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)
        # Opslaan van alle volumes
        # pytsk3 is globaal, en werkt voor alle ingeladen images. Om deze rede is de functie get_partitions() gemaakt
        # Deze kan onderscheid maken tussen de volumes van verschillende images
        self.volumes = pytsk3.Volume_Info(self)

        DebugLog("Loading Partitions")

        # Doorlopen van partitielijst en partities opslaan in geheugen
        for partition in self.volumes:
            # Alleen voor partities groter dan 2048kb
            if partition.len > 2048:
                # Waarvan de omschrijving niet is: Unallocated, Extended, Primary Table.
                # Deze partitie types bevatten geen gebruikbare data
                if "Unallocated" not in partition.desc and "Extended" not in partition.desc and "Primary Table" not in partition.desc:
                    self.partities.append(
                        FSParInfo(partition, self.volumes, self, self.image))

    # Pytsk3 deelt alle volumes van alle ingeladen images
    # Hiervoor moet iedere partitie worden gecontroleerd met de ingladen image
    # Waaruit een lijst wordt teruggestuurd met alleen de partities van deze image.
    def get_partitions(self):
        partitions = []
        for part in self.partities:
            # Controleren of image path het zelfde is als huidige image (om foutieve resultaten uit te sluiten)
            if part.image.image_path is self.image.image_path:
                partitions.append(part)
        return partitions

    # Ophalen van partitie d.m.v. het unieke adres
    # Extra functionaliteit nodig voor het uitvoeren van web interface
    def get_partition(self, addr):
        for part in self.get_partitions():
            if part.addr is addr:
                return part

    # Afsluiten van de ewf stream
    def close(self):
        self.ewf_handle.close()

    # Lezen van bytes uit image.
    # Offset is de positie waarvandaan het lezen moet worden gestart
    # Size is de lengte waarvan er gelezen moet worden
    def read(self, offset, size):
        self.ewf_handle.seek(offset)
        return self.ewf_handle.read(size)

    # Uitlezen van de partitie grootte
    def get_size(self):
        return self.ewf_handle.get_media_size()

    # Printen van een lijst met alle partities
    def partition_report(self):
        partition_array = []

        for count in range(len(self.get_partitions())):
            partition_array.append([count, self.get_partitions()[
                                   count].len, self.get_partitions()[count].desc])

        print tabulate(partition_array, headers=[
                       "Addr", "Size", "Description"])
        print ''
