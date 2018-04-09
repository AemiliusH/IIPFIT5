
from Image.Image import *
from Modules.bestand import *
from Modules.browser import *
from Modules.foto import *
#from Web.Web import *
from Utils.FileType import *

header = '''    ______                           _         ______            ____   _ __ 
   / ____/___  ________  ____  _____(_)____   /_  __/___  ____  / / /__(_) /_
  / /_  / __ \/ ___/ _ \/ __ \/ ___/ / ___/    / / / __ \/ __ \/ / //_/ / __/
 / __/ / /_/ / /  /  __/ / / (__  ) / /__     / / / /_/ / /_/ / / ,< / / /_  
/_/    \____/_/   \___/_/ /_/____/_/\___/    /_/  \____/\____/_/_/|_/_/\__/  
                                                                             '''


class Hoofdmenu():

    # Instanties van losse modules
    logger = None
    bestand = None
    exception = None
    foto = None
    browser = None
    case = None
    sql = None

    # Lijst van ingeladen images
    images = []

    def __init__(self):
        # Handmatig toevoegen van images d.m.v. path naar file
        self.images.append(
            Image('C:\\Users\\0x000000\\Documents\\LCB\\USBKOPIEroze16GB.E01'))
        self.images.append(Image(
            'C:\\Users\\0x000000\\Documents\\School\\Hogeschool Leiden\\Jaar 2\\IPFIT5\\Images\\sample_image_01.E01'))
        self.images.append(Image(
            'C:\\Users\\0x000000\\Documents\\School\\Hogeschool Leiden\\Jaar 2\\IPFIT5\\Images\\sample_image_02.E01'))

        # Initaliseren van individuele modules
        self.bestand = Bestand(self)
        self.browser = Browser(self)
        self.foto = Foto(self)
        self.cli()
        # Optioneel: Websocket
        #self.web = Socket(5002, 'Forensic Toolkit', self)

      # self.web.run(False)

    def add_image(self, path):
        '''
        Image Toevoegen aan case
        :param path: Path naar bestand
        :return: None
        '''
        # Toevoegen image aan hoofdmenu
        self.images.append(Image(path))

    def cli(self):
        '''
        Command Line Interface voor application
        :return: None
        '''
        self.print_header()
        # Commandline interface blijft beschikbaar door loop
        # Vanuit commandline kan worden aangegeven welke module moet worden gestart
        while True:
            # Printen van alle opties
            print ''
            print '\t[1] Bestand'
            print '\t[2] Browser'
            print '\t[3] Foto'
            print '\t[4] Add Image File (dd/E01)'
            print '\t[0] Exit'

            # Uitlezen gebruikersinput
            input = int(raw_input('Please choose an option [0-9]: '))

            # Input verwerken en aanroepen juiste functie
            if input == 1:
                self.bestand.run()
            if input == 2:
                self.browser.run()
            if input == 3:
                self.foto.run()
            if input == 4:
                self.images.append(Image(raw_input("Path: ")))
            if input == 0:
                exit(1)

    def print_header(self):
        '''
        Printen van het mooie logo
        :return: None
        '''
        print header


# Inialiseren van hoofdmenu
Hoofdmenu()
