
from Image.Image import *
from Utils.Models import *
from Modules.bestand import *
from Modules.browser import *
from Modules.foto import *
from Utils.Database import *
from Utils.log import *
#from Web.Web import *
from Utils.FileType import *

header = '''    ______                           _         ______            ____   _ __ 
   / ____/___  ________  ____  _____(_)____   /_  __/___  ____  / / /__(_) /_
  / /_  / __ \/ ___/ _ \/ __ \/ ___/ / ___/    / / / __ \/ __ \/ / //_/ / __/
 / __/ / /_/ / /  /  __/ / / (__  ) / /__     / / / /_/ / /_/ / / ,< / / /_  
/_/    \____/_/   \___/_/ /_/____/_/\___/    /_/  \____/\____/_/_/|_/_/\__/  
                                                                             '''


class Hoofdmenu:

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
        print header
        # Initaliseren van individuele modules
        self.database = Database(self)
        Debugger('Initalising Modules!')

        self.bestand = Bestand(self)
        self.browser = Browser(self)
        self.foto = Foto(self)

        Debugger('Done initalising Modules!')
        Debugger('Running user CLI')

        self.database.run()
        self.cli()



        # Optioneel: Websocket
        #self.web = Socket(5002, 'Forensic Toolkit', self)

      #  self.web.run(False)

    def add_image(self, path):
        # Toevoegen image aan hoofdmenu
        Logger('Adding Image: ' + str(path))
        self.images.append(Image(path))

    def cli(self):
        # self.database.run()
        # Commandline interface blijft beschikbaar door loop
        # Vanuit commandline kan worden aangegeven welke module moet worden gestart

        while True:
            try:
                # Printen van alle opties
                print ''
                print '\t[1] Bestand'
                print '\t[2] Browser'
                print '\t[3] Foto'
                print '\t[4] Add Image File'
                print '\t[5] Logboek'
                print '\t[0] Exit'

                Debugger('Main Menu')
                # Uitlezen gebruikersinput
                input = int(raw_input('Please choose an option [0-9]: '))
                Debugger('Selected Option: ' + str(input))
                # Input verwerken en aanroepen juiste functie
                if input == 1:
                    self.bestand.run()
                if input == 2:
                    self.browser.run()
                if input == 3:
                    self.foto.run()
                if input == 4:
                    self.database.add_image()
                if input == 5:
                    self.logboek()
                if input == 0:
                    Debugger('Exiting Program...', True)
                    exit(1)
            except:
                ErrorLogger()

    def print_header(self):
        print header

    def logboek(self):
        logger = self.database.get_log()

        print '\t[0] Print Logboek'
        print '\t[1] Store to CSV'

        log_array = []
        for log in logger:
            log_array.append([str(log.ID), log.Handeling, log.Datum])

        inp = int(raw_input('Maak een keuze [0-9] '))
        if inp == 0:
            print tabulate(log_array, headers=['ID', 'Handeling', 'Datum'])
        else:
            self.bestand.save_array_to_csv(
                log_array, 'ID;Handeling;Datum\n')



# Inialiseren van hoofdmenu
Hoofdmenu()
