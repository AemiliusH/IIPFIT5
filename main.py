
from Image.Image import *
from Modules.bestand import *
from Modules.browser import *
from Modules.foto import *

from Utils.FileType import * 

header = '''    ______                           _         ______            ____   _ __ 
   / ____/___  ________  ____  _____(_)____   /_  __/___  ____  / / /__(_) /_
  / /_  / __ \/ ___/ _ \/ __ \/ ___/ / ___/    / / / __ \/ __ \/ / //_/ / __/
 / __/ / /_/ / /  /  __/ / / (__  ) / /__     / / / /_/ / /_/ / / ,< / / /_  
/_/    \____/_/   \___/_/ /_/____/_/\___/    /_/  \____/\____/_/_/|_/_/\__/  
                                                                             '''

class Hoofdmenu(): 
    logger = None
    bestand = None
    exception = None
    foto = None
    browser = None
    case = None
    sql = None

    images = []

    def __init__(self):
        self.images.append(Image('C:\\Users\\0x000000\\Documents\\LCB\\USBKOPIEroze16GB.E01'))
        self.images.append(Image('C:\\Users\\0x000000\\Documents\\School\\Hogeschool Leiden\\Jaar 2\\IPFIT5\\Images\\sample_image_01.E01'))
  
        self.bestand = Bestand(self)
        self.browser = Browser(self)
        self.foto = Foto(self)
  
        self.print_header()
        self.bestand.run()

    def cli(self):
        while True:

            print ''
            print '\t[0] Bestand'
            print '\t[1] Browser'
            print '\t[2] Foto'

            input = int(raw_input('Please choose an option [0-9]: '))

            if input == 0:
                self.bestand.run()
            if input == 1:
                self.browser.run()
            if input == 2:
                self.foto.run()

    def print_header(self):
        print header


    
Hoofdmenu()




  

#image = Image("C:\\Users\\0x000000\\Documents\\School\\Hogeschool Leiden\\Jaar 2\\IPFJURI\\Bewijs\\USBKOPIEroze16GB.E01")






'''class EWFImgInfo(pytsk3.Img_Info):
        def __init__(self, ewf_handle):
            self._ewf_handle = ewf_handle
            super(EWFImgInfo, self).__init__(
                url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

        def close(self):
            self._ewf_handle.close()

        def read(self, offset, size):
            self._ewf_handle.seek(offset)
            return self._ewf_handle.read(size)

        def get_size(self):
            return self._ewf_handle.get_media_size() 

class FileInfo:
    def __init__(self, name, size, hash, extention):
        self.name = name
        self.size = size
        self.hash = hash
        self.extention = extention

filelist = []

filepath = "C:\\Users\\0x000000\\Documents\\School\\Hogeschool Leiden\\Jaar 2\\IPFJURI\\Bewijs\\USBKOPIEroze16GB.E01"

filenames = pyewf.glob(filepath)

ewf_handle = pyewf.handle()
ewf_handle.open(filenames)

img_info = EWFImgInfo(ewf_handle)
vol = pytsk3.Volume_Info(img_info) 

for part in vol:
    if part.len > 2048 and "Unallocated" not in part.desc \
            and "Extended" not in part.desc \
            and "Primary Table" not in part.desc:
        try:
            fs = pytsk3.FS_Info(img_info, offset=part.start * vol.info.block_size)
        except IOError:
            _, e, _ = sys.exc_info()
            print("[-] Unable to open FS:\n {}".format(e))
        root = fs.open_dir(path="/") 

        # Voor ieder bestand
        for fs_object in root: 
            try:
                file_size = getattr(fs_object.info.meta, "size", 0)
                file_name = fs_object.info.name.name 

                hash_obj = hashlib.md5()
                hash_obj.update(fs_object.read_random(0, file_size))
 
                header = fs_object.read_random(0, 4) 
                extention = extentions()
                file_extention = extention.find_extention(header) 

                filelist.append([file_name, file_size, hash_obj.hexdigest(), file_extention]) 
            except Exception as e: 
                print e '''

                
 


#print tabulate(filelist, headers=['Bestandsnaam', 'Size', 'MD5', 'extention'])