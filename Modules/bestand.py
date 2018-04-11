import pyewf
import pytsk3
import binascii
import datetime
import re

from StringIO import StringIO
from tabulate import tabulate
from zipfile import ZipFile

from Utils.FileType import *
from Utils.VirusToal import *


class Bestand():

    def __init__(self, main):
        '''
        Individuele bestand's module. Voert bewerkingen uit op Images
        :param main: Referentie naar hoofdmenu
        '''
        # Referentie naar hoofdmenu opslaan
        self.main = main

    def generate_hashlist(self):
        '''
        Genereerd een lijst met alle hashes van geselecteerde partitie
        :return: None
        '''
        # Gebruiker een partitie uit een image laten selecteren
        partitie = self.select_partition()
        # Array van bestanden opslaan
        files = partitie.files
        # Nieuwe array maken om metadata per file op te lsaan
        array_list = []
        # Voor iedere file meta-data opslaan naar array_list
        for file in files:
            array_list.append(file.get_attributes())

        print '\t[0] Print List'
        print '\t[1] Export List (CSV)'

        # Input van gebruiker lezen
        result = int(raw_input('\nPlease choose an option[0-9]: '))

        if result == 0:
            # Printen van mooie tabel
            print tabulate(array_list, headers=[
                           'Name', 'Size', 'Created', 'Changed', 'Modified', 'MD5', 'SHA256'])
            self.main.database.write_log("Heeft een lijst van hashes gegenereert op het scherm")
        else:
            # Wegschrijven van data naar .csv file
            self.save_array_to_csv(
                array_list, 'Name;Size;Created;Changed;Modified;MD5;SHA256\n')
            self.main.database.write_log("Heeft een lijst van hashes geexporteerd als CSV")



    def generate_timeline(self):
        '''
        Genereerd lijst met alle bestanden van partitie in geselecteerde volgorde
        :return: None
        '''
        # Gebruiker een partitie uit image laten selecteren
        partitie = self.select_partition()

        # Gebruikers input uitlezen
        print 'Please select on what value to order:'
        print '\t[0] File Created'
        print '\t[1] File Modified'
        print '\t[2] File Changed'
        type = int(raw_input('\nPlease Choose an option [0-9]: '))

        print '\t[0] Oldest First'
        print '\t[1] Newest First'
        order = bool(int(raw_input('\nPlease choose an option[0-9]: ')))

        print 'Generating List......'
        # Array voor files met meta-data
        timeline = []
        # referentie naar file array opslaan
        files = partitie.files

        for file in files:
            timeline.append((file.create, file.modify, file.change, file))

        # timelijn sorteren op type (created/modified/changed) in juiste volgorde (nieuwste eerst/laatste eerst)
        timeline = sorted(timeline, key=lambda x: x[type], reverse=order)

        # Voor alle files in juiste volgorde de attributes opslaan
        array_list = []
        for file in timeline:
            array_list.append(file[3].get_attributes())

        print '\t[0] Print Timeline'
        print '\t[1] Export Timeline (CSV)'
        # Gebruikersinput afhandelen
        result = int(raw_input('\nPlease choose an option[0-9]: '))

        if result == 0:
            # Mooie tabel printen
            print tabulate(array_list, headers=[
                           'Name', 'Size', 'Created', 'Changed', 'Modified', 'MD5', 'SHA256'])
            self.main.database.write_log("Heeft een TimeLine op het Scherm geprint")
        else:
            # Data wegschrijven naar csv
            self.save_array_to_csv(
                array_list, 'Name;Size;Created;Changed;Modified;MD5;SHA256\n')
            self.main.database.write_log("Heeft een TimeLine weggeschreven naar CSV")


    def save_array_to_csv(self, array, head):
        '''
        Functie om dubbele array weg te schrijven naar CSV
        :param array: Array met data
        :param head: Array met header namen
        :return: None
        '''
        # Bestandsnaam vragen aan gebruiker
        filename = raw_input('\nEnter Filename: ')
        # Referentie naar bestand openen (bestandsnaam + .csv)
        file = open(filename + '.csv', 'w')
        # Wegschrijven 'header', dit is de eerste regel met column informatie
        file.write(head + '\n')
        # Voor ieder object in de array, de subonderdelen wegschrijven als .csv door ; te gebruiken
        for obj in array:
            file.write(';'.join(str(e) for e in obj) + '\n')

    def select_partition(self):
        '''
        Funcite om gebruiker een partitie te laten selecteren
        :return: Geselecteerde FSParInfo object
        '''
        print 'Please select an image: '
        # printen van iedere image, met path. Waarvan de ID overeenkomt met de array positie
        for a in range(len(self.main.images)):
            print '\t[' + str(a) + '] ' + self.main.images[a].image_path

        # Gebruiker de image laten selecteren
        image = int(raw_input('\nPlease Choose an option [0-9]: '))
        print 'Please select an Partition: '
        # Printen van alle partities van geselecteerde image
        # Met informatie over de grootte van de paritie MB en de partitie ID
        for part in range(len(self.main.images[image].ewf_img_info.get_partitions())):
            partition_pointer = self.main.images[image].ewf_img_info.get_partitions()[
                part]
            print '\t[' + str(part) + '] ' + partition_pointer.desc + \
                " - " + str(partition_pointer.size / 1024) + "MB"

        # Gebruiker's input afhandelen
        part = int(raw_input('\nPlease Choose an option [0-9]: '))

        # returnen van partitie object
        return self.main.images[image].ewf_img_info.get_partitions()[part]


    def select_file(self):
        '''
        Functie om gebruiker een file te laten selecteren
        :return: Geselecteerde FSFileInfo object
        '''
        # Gebruiker een partiie laten selecteren
        partitie = self.select_partition()
        # Printing all files with ID
        for file in range(len(partitie.files)):
            try:
                print '\t[' + str(file) + '] ' + partitie.files[file].name
            except:
                pass
        file = int(raw_input('\nPlease select an file: '))
        # Getting object of selected file
        return partitie.files[file]

    def detect_language(self):
        '''
        Detecteerd taal per bestand
        :return: None
        '''
        # Getting object of selected file
        file_handle = self.select_file()

        # Printing basic information
        print '==' * 30
        print 'Filename:\t' + file_handle.name
        print 'SHA1:\t\t' + str(file_handle.sha1())
        print 'SHA256:\t\t' + str(file_handle.sha256())

        # Requested language from file
        file_handle.print_language_table()
        print '==' * 30
        self.main.database.write_log("Heeft gezocht naar gebruikte talen")

    def generate_ziplist(self):
        '''
        Genereerd een lijst van alle bestanden in ZIP file
        Gebaseerd op gebruikersinput
        :return: None
        '''
        # gebruiker een partiie laten selecteren
        partitie = self.select_partition()
        ziplist = []

        # Lijst met zipfiles genereren
        for a in range(len(partitie.files)):
            if partitie.files[a].get_extention()[0] is 'ZIP':
                print '\t[' + str(len(ziplist)) + ']  \t' + \
                    partitie.files[a].name
                ziplist.append(partitie.files[a])

        # Gebruiker de zipfile laten selecteren
        zip_id = int(raw_input("Please select an zipfile [0-9]"))
        file_handle = ziplist[zip_id]

        # Geselecteerde zipfile openen als virtueel bestand met StringIO
        zip = ZipFile(StringIO(file_handle.read_raw_bytes()))
        zip_array = []
        # Infolist ophalen van zipfile
        # Bestanden opslaan in zip_array om deze informatie te kunnen verwerken
        for info in zip.infolist():
            zip_array.append([info.filename, datetime.datetime(
                *info.date_time), info.file_size])

        print '\t[0] Print Filetypes'
        print '\t[1] Export Filetypes (CSV)'

        # Gebruikersinput ophalen
        input = int(raw_input('\nPlease Choose an option [0-9]: '))
        if input == 0:
            # Mooie tabel printen
            print tabulate(zip_array, headers=['Filename', 'Created', 'Size'])
            self.main.database.write_log("Heeft een lijst van Zips op het scherm geprint")
        else:
            # Data wegschrijven naar .csv
            self.save_array_to_csv(zip_array, 'Filename;Created;Size')
            self.main.database.write_log("Heeft een lijst van Zips geexporteerd")

        zip.close()

    def generate_filetypelist(self):
        '''
        Genereerd een lijst met filetypes
        Gebaseerd op gebruikresinput
        :return: None
        '''
        # alle files ophalen uit geselecteerde partitie
        files = self.select_partition().files
        file_array = []
        # Iedere file analyseren
        # Alle bekende files wegschrijven naar file_array
        # Wanneeer deze onbekend is de file name gebruiken als extentie
        for file in files:
            type = FileType(file).analyse()
            if type[1] is not '':
                type.append(file.name)
                file_array.append(type)

        print '\t[0] Print Filetypes'
        print '\t[1] Export Filetypes (CSV)'

        # Gebruikers input opnemen
        input = int(raw_input('\nPlease Choose an option [0-9]: '))
        if input == 0:
            # Printen mooie tabel
            print tabulate(file_array, headers=[
                           'Extention', 'Description', 'Filename'])
            self.main.database.write_log("Heeft een lijst van Filetypes geprint op het scherm")
        else:
            # data wegschrijven naar .csv
            self.save_array_to_csv(
                file_array, 'Extention;Description;FileName')
            self.main.database.write_log("Heeft een lijst van Filetypes weggeschreven naar CSV")


    def cli(self):
        '''
        CommandLineInterface Vanuit hier wordt de module aangestuurd
        :return: None
        '''
        while True:
            print ''
            print ' ' + '==' * 22
            print '|                  Bestand                   |'
            print ' ' + '==' * 22
            print ''
            print "\t[1] Generate Hashlist"
            print '\t[2] List ZIP/Archives'
            print '\t[3] Generate Timeline'
            print '\t[4] List Filetypes'
            print '\t[5] Find Used Languages'
            print '\t[6] Export File'
            print '\t[7] VirusTotal'
            print '\t[8] Back'
            print ''

            # Gebruikersinput uitlezen
            input = int(raw_input('Please choose an option [0-9]: '))
            # Aanroepen juiste functie
            if input == 1:
                self.generate_hashlist()
            if input == 2:
                self.generate_ziplist()
            if input == 3:
                self.generate_timeline()
            if input == 4:
                self.generate_filetypelist()
            if input == 5:
                self.detect_language()
            if input == 6:
                self.export_file()
            if input == 7:
                self.virustotal_file()
            if input == 8:
                break


    def virustotal_file(self):
        '''
        Bestand door virustotal halen
        :return: None
        '''
        # Gebruiker een bestand laten selecteren
        file = self.select_file()
        # Virustotal class gebruiken
        total = VirusTotal(file).lookup_hash()


    def export_file(self):
        '''
        Geselecteerd bestand exporteren
        :return: None
        '''
        self.select_file().export()


    def run(self):
        '''
        Starten van Bestand's module
        :return: None
        '''
        # Wanneer er geen bruikbare images zijn terugkeren naar hoofdmenu
        if len(self.main.images) == 0:
            print "Please import an image before using modules!"
        else:
            # Command Line Interface starten
            self.cli()


    def generate_hashlist_api(self, image, partitie):
        '''
        Ongeimplementeerde API Funcites voor webinterface
        :param image: Image ID
        :param partitie: Partitie ID
        :return: Array met hashes
        '''
        img = self.main.images[image]
        par = img.ewf_img_info.get_partition(partitie)
        arr = []
        for file in par.files:
            arr.append(file.get_attributes())
        return arr

    def generate_ziplist_api(self, image, partitie):
        '''
        Ongeimplementeerde API Funcites voor webinterface
        :param image: Image ID
        :param partitie: Partitie ID
        :return: Array met zipfiles
        '''
        img = self.main.images[image]
        par = img.ewf_img_info.get_partition(partitie)
        arr = []

        for a in range(len(par.files)):
            if par.files[a].get_extention()[0] is 'ZIP':
                file = par.files[a]
                arr.append(file.get_attributes())
        return arr
