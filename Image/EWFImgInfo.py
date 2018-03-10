import pytsk3
import pyewf

from FSParInfo import *
from Utils.log import *

class EWFImgInfo(pytsk3.Img_Info):
    partities = [] 

    def __init__(self, ewf_handle):
        self.ewf_handle = ewf_handle
        super(EWFImgInfo, self).__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL) 
        self.volumes = pytsk3.Volume_Info(self) 
        
        DebugLog("Loading Partitions") 

        #Loading Partitions into memory
        for partition in self.volumes:
            if partition.len > 2048:
                if "Unallocated" not in partition.desc and "Extended" not in partition.desc and "Primary Table" not in partition.desc:
                    self.partities.append(FSParInfo(partition, self.volumes, self))
     
    def close(self):
        self.ewf_handle.close()

    def read(self, offset, size):
        self.ewf_handle.seek(offset)
        return self.ewf_handle.read(size)

    def get_size(self):
        return self.ewf_handle.get_media_size()

    def partition_report(self): 
        partition_array = [] 

        for count in range(len(self.partities)):
            partition_array.append([count, self.partities[count].len, self.partities[count].desc]) 
  
        print tabulate(partition_array, headers=["Addr", "Size", "Description"])
        print ''
 