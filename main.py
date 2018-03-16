
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
# Curses python windows


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
        self.images.append(
            Image('C:\\Users\\0x000000\\Documents\\LCB\\USBKOPIEroze16GB.E01'))
        self.images.append(Image(
            'C:\\Users\\0x000000\\Documents\\School\\Hogeschool Leiden\\Jaar 2\\IPFIT5\\Images\\sample_image_01.E01'))
        self.images.append(Image(
            'C:\\Users\\0x000000\\Documents\\School\\Hogeschool Leiden\\Jaar 2\\IPFIT5\\Images\\sample_image_02.E01'))
        #self.images.append(Image('D:\\Test_image_5.E01'))
        self.bestand = Bestand(self)
        self.browser = Browser(self)
        self.foto = Foto(self)

        self.print_header()
        self.cli()

    def is_ascii(self, s):
        return all(ord(c) < 128 for c in s)

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
        print bcolors.HEADER + header + bcolors.ENDC


Hoofdmenu()
