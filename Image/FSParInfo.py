import pytsk3
import pyewf

from tabulate import tabulate
from EWFImgInfo import *
from FSFileInfo import *


class FSParInfo():
    def __init__(self, partition_handle, volume_info, image_info, image):
        #self.ewf_handle = ewf_handle
        self.image = image
        self.partition_handle = partition_handle
        self.volume_info = volume_info 
        self.image_info = image_info

        self.size = self.partition_handle.len
        self.desc = self.partition_handle.desc 
        self.addr = self.partition_handle.addr
        self.len = self.partition_handle.len
        self.dirs = []
        self.files = []

        try:
            self.fs_handle = pytsk3.FS_Info(self.image_info, offset=self.partition_handle.start * self.volume_info.info.block_size)
        except IOError:
            print "Error: Kan FS Niet openen"
        
        DebugLog("Succesfully Mounted FileSystem!")
        
        self.root = self.fs_handle.open_dir(path="/") 
        self.recurse_files() 

        DebugLog("{} Dirs and {} Files located".format(str(len(self.dirs)), str(len(self.files))))
 
    def get_root(self):
        self.root = self.fs_handle.open_dir(path="/")

    def recurse_dir(self, dir, parent):
        self.dirs.append(dir.info.meta.addr)
        parent = parent  + dir.info.name.name + '\\'
        dir = dir.as_directory()
        for object in dir:
            try:  
                if object.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                    #Creating nested loop!
                    if object.info.meta.addr not in self.dirs:
                        self.recurse_dir(object, parent)
                else:
                    self.files.append(FSFileInfo(object, parent))
            except AttributeError:
                DebugLog('Error parsing Object: ' + object.info.name.name)

    def recurse_files(self):
        self.dirs.append(self.root.info.fs_file.meta.addr)
        parent = "\\"
        #Nested loop voor het uitlezen van mappen in mappen
        for object in self.root: 
            try:
                if object.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                    self.recurse_dir(object, parent)
                else: 
                    self.files.append(FSFileInfo(object, parent))
            except AttributeError: 
                DebugLog('Error parsing Object: ' + object.info.name.name)
         
    def files_rapport(self):
        attribute_array = []
        for object in self.files:
            attribute_array.append(object.get_attributes())
 
        print tabulate(attribute_array, headers=['Path', 'Name', 'Size', 'Created', 'Changed', 'Modified', 'MD5', 'SHA256'])

    def size(self):
        return ewf_handle.media_size()
