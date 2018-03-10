from EWFImgInfo import *

class Image():
    ewf_img_info = None
    def __init__(self, image_path):

        DebugLog("Loading image from: " + image_path)

        self.image_path = image_path

        #Opening Image in pyEWF
        self.image_files = pyewf.glob(self.image_path)
        self.ewf_handle = pyewf.handle()
        self.ewf_handle.open(self.image_files)

        #Creating Object for Image
        self.ewf_img_info = EWFImgInfo(self.ewf_handle)
 
        DebugLog("Image succesfully loaded!")

        #self.ewf_img_info.partition_report() 
         
    def get_all_files(self):
        files = []
        for partitie in self.ewf_img_info.partities:
            files.extend(partitie.files)

        return files

