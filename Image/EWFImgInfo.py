import pytsk3
import pyewf

from FSParInfo import *
from Utils.log import *


class EWFImgInfo(pytsk3.Img_Info):
    partities = []

    def __init__(self, ewf_handle, image):
        self.image = image
        self.ewf_handle = ewf_handle
        super(EWFImgInfo, self).__init__(
            url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)
        self.volumes = pytsk3.Volume_Info(self)

        DebugLog("Loading Partitions")

        # Loading Partitions into memory
        for partition in self.volumes:
            if partition.len > 2048:
                if "Unallocated" not in partition.desc and "Extended" not in partition.desc and "Primary Table" not in partition.desc:
                    self.partities.append(
                        FSParInfo(partition, self.volumes, self, self.image))

    # Pytsk3 shares volumes from different images
    # Checking for each partition the path of origin image against requested image
    # Returning a list with all paritions of this spesific image
    def get_partitions(self):
        partitions = []
        for part in self.partities:
            if part.image.image_path is self.image.image_path:
                partitions.append(part)
        return partitions

    def close(self):
        self.ewf_handle.close()

    def read(self, offset, size):
        self.ewf_handle.seek(offset)
        return self.ewf_handle.read(size)

    def get_size(self):
        return self.ewf_handle.get_media_size()

    def partition_report(self):
        partition_array = []

        for count in range(len(self.get_partitions())):
            partition_array.append([count, self.get_partitions()[
                                   count].len, self.get_partitions()[count].desc])

        print tabulate(partition_array, headers=[
                       "Addr", "Size", "Description"])
        print ''
