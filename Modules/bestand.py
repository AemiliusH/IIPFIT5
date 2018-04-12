import pyewf
import pytsk3
import binascii
import datetime
import re
import os

from StringIO import StringIO
from tabulate import tabulate
from zipfile import ZipFile

from Utils.FileType import *
from Utils.VirusToal import *
from Utils.log import *


class Bestand():

    def __init__(self, main):
        '''
        Individuele bestand's module. Voert bewerkingen uit op Images
        :param main: Referentie naar hoofdmenu
        '''
        # Referentie naar hoofdmenu opslaan
        self.main = main

    def UserInput(self, options):
        while True:
            for a in range(len(options)):
                print '\t [' + str(a) + '] ' + str(options[a])
            try:
                input = int(raw_input('Please select an option [0-' + str(len(options) - 1) + ']: '))
                if input in range(len(options)):
                    return input
            except:
                print ''
                pass

    def isValid(self, value, options):
        try:
            if value in options:
                return True
            else:
                print '\tPlease select an valid option: ' + options
                return False
        except:
            ErrorLogger()

    def generate_hashlist(self):
        '''
        Genereerd een lijst met alle hashes van geselecteerde partitie
        :return: None
        '''
        try:
            Debugger('Generating Hashlist...')
            # Gebruiker een partitie uit een image laten selecteren
            partitie = self.select_partition()
            # Array van bestanden opslaan
            files = partitie.files
            # Nieuwe array maken om metadata per file op te lsaan
            array_list = []
            # Voor iedere file meta-data opslaan naar array_list
            for file in files:
                array_list.append(file.get_attributes())

            result = self.UserInput(['Print List', 'Export List (CSV)'])

            if result == 0:
                # Printen van mooie tabel
                Debugger('Printing hashlist')
                print tabulate(array_list, headers=[
                               'Name', 'Size', 'Created', 'Changed', 'Modified', 'MD5', 'SHA256'])

            else:
                # Wegschrijven van data naar .csv file
                Debugger('Storing Hashlist as CSV')
                self.save_array_to_csv(
                    array_list, 'Name;Size;Created;Changed;Modified;MD5;SHA256\n')
        except:
            ErrorLogger(True)

    def generate_timeline(self):
        '''
        Genereerd lijst met alle bestanden van partitie in geselecteerde volgorde
        :return: None
        '''

        try:
            # Gebruiker een partitie uit image laten selecteren
            Debugger('Generating Timeline')

            partitie = self.select_partition()

            # Gebruikers input uitlezen
            print 'Please select on what value to order:'
            type = self.UserInput(['File Created', 'File Modified', 'File Changed'])
            Debugger('Selected type: ' + str(type))

            order = self.UserInput(['Oldest First','Newest First'])


            Debugger('Selected order: ' + str(order))
            Logger('Genereating Timeline...')
            # Array voor files met meta-data
            timeline = []
            # referentie naar file array opslaan
            files = partitie.files
            hash_base = []
            for file in files:
                hash = file.md5()
                if hash not in hash_base:
                    timeline.append((file.create, file.modify, file.change, file))
                    hash_base.append(hash)

            # timelijn sorteren op type (created/modified/changed) in juiste volgorde (nieuwste eerst/laatste eerst)
            timeline = sorted(timeline, key=lambda x: x[type], reverse=order)

            # Voor alle files in juiste volgorde de attributes opslaan
            array_list = []
            for file in timeline:
                array_list.append(file[3].get_attributes())

            result = self.UserInput(['Print Timeline', 'Export Timeline (CSV)'])

            if result == 0:
                Debugger('Printing Timetable')

                # Mooie tabel printen
                print tabulate(array_list, headers=[
                               'Name', 'Size', 'Created', 'Changed', 'Modified', 'MD5', 'SHA256'])
                Debugger("Printing timeline on console")
            else:

                Debugger('Storing timetable as CSV')
                # Data wegschrijven naar csv
                self.save_array_to_csv(
                    array_list, 'Name;Size;Created;Changed;Modified;MD5;SHA256\n')
                Debugger('Writing timeline to CSV')
        except:
            ErrorLogger(True)

    def save_array_to_csv(self, array, head):
        '''
        Functie om dubbele array weg te schrijven naar CSV
        :param array: Array met data
        :param head: Array met header namen
        :return: None
        '''

        try:
            # Bestandsnaam vragen aan gebruiker
            filename = raw_input('\nEnter Filename: ')

            Debugger('Writing CSV data to: ' +
                     str(os.path.dirname(os.path.abspath(__file__))) + ' - ' + filename + '.csv')
            # Referentie naar bestand openen (bestandsnaam + .csv)
            file = open(filename + '.csv', 'w')
            # Wegschrijven 'header', dit is de eerste regel met column informatie
            file.write(head + '\n')
            # Voor ieder object in de array, de subonderdelen wegschrijven als .csv door ; te gebruiken
            for obj in array:
                file.write(';'.join(str(e) for e in obj) + '\n')

            Debugger('Succesfully Written!')
        except:
            ErrorLogger(True)

    def select_partition(self):
        '''
        Funcite om gebruiker een partitie te laten selecteren
        :return: Geselecteerde FSParInfo object
        '''
        try:
            print 'Please select an image: '
            images = []
            # printen van iedere image, met path. Waarvan de ID overeenkomt met de array positie
            for a in range(len(self.main.images)):
                images.append(self.main.images[a].image_path)

            image = self.UserInput(images)


            Debugger('Selected Image: ' + self.main.images[image].image_path)


            print 'Please select an Partition: '
            # Printen van alle partities van geselecteerde image
            # Met informatie over de grootte van de paritie MB en de partitie ID
            partitions = []
            for part in range(len(self.main.images[image].ewf_img_info.get_partitions())):
                partition_pointer = self.main.images[image].ewf_img_info.get_partitions()[
                    part]
                partitions.append(partition_pointer.desc + " - " + str(partition_pointer.size / 1024) + "MB")

            part = self.UserInput(partitions)

            Debugger('Selected Partition: ' + str(part) + ' ' +
                     str(self.main.images[image].ewf_img_info.get_partitions()[part].desc))
            # returnen van partitie object
            return self.main.images[image].ewf_img_info.get_partitions()[part]
        except:
            ErrorLogger(True)

    def select_file(self):
        '''
        Functie om gebruiker een file te laten selecteren
        :return: Geselecteerde FSFileInfo object
        '''
        # Gebruiker een partiie laten selecteren
        partitie = self.select_partition()
        # Printing all files with ID
        files = []
        for file in range(len(partitie.files)):
            try:
                files.append(partitie.files[file].name)
            except:
                pass
        file = self.UserInput(files)
        Debugger('Selected File: ' + str(file) +
                 ' ' + str(partitie.files[file].name))
        # Getting object of selected file
        return partitie.files[file]

    def detect_language(self):
        '''
        Detecteerd taal per bestand
        :return: None
        '''
        Debugger('Finding Language For file')
        # Getting object of selected file
        file_handle = self.select_file()

        # Printing basic information
        print '==' * 30
        print 'Filename:\t' + file_handle.name
        print 'SHA1:\t\t' + str(file_handle.sha1())
        print 'SHA256:\t\t' + str(file_handle.sha256())

        Debugger('Printing Language table to console')
        # Requested language from file
        file_handle.print_language_table()
        print '==' * 30

    def generate_ziplist(self):
        '''
        Genereerd een lijst van alle bestanden in ZIP file
        Gebaseerd op gebruikersinput
        :return: None
        '''
        Debugger('Generating ZIP list')

        # gebruiker een partiie laten selecteren
        partitie = self.select_partition()
        ziplist = []

        Debugger('Finding all ZIP\'s from Partition')

        zips = []
        # Lijst met zipfiles genereren
        for a in range(len(partitie.files)):
            if partitie.files[a].get_extention()[0] is 'ZIP':
                zips.append(partitie.files[a].name)
                ziplist.append(partitie.files[a])

        # Gebruiker de zipfile laten selecteren
        zip_id = self.UserInput(zips)

        Debugger('Selected ZIP with ID: ' + str(zip_id))
        file_handle = ziplist[zip_id]

        # Geselecteerde zipfile openen als virtueel bestand met StringIO
        zip = ZipFile(StringIO(file_handle.read_raw_bytes()))
        zip_array = []
        # Infolist ophalen van zipfile
        # Bestanden opslaan in zip_array om deze informatie te kunnen verwerken
        for info in zip.infolist():
            zip_array.append([info.filename, datetime.datetime(
                *info.date_time), info.file_size])


        input = self.UserInput(['Print Filetypes','Export Filetypes (CSV)'])


        if input == 0:
            Debugger('Printing ZIP List')
            # Mooie tabel printen
            print tabulate(zip_array, headers=['Filename', 'Created', 'Size'])

        else:
            Debugger('Writing ZIP list to CSV')
            # Data wegschrijven naar .csv
            self.save_array_to_csv(zip_array, 'Filename;Created;Size')

        zip.close()

    def generate_filetypelist(self):
        '''
        Genereerd een lijst met filetypes
        Gebaseerd op gebruikresinput
        :return: None
        '''

        Debugger('Generating Filetypelist')
        # alle files ophalen uit geselecteerde partitie
        files = self.select_partition().files
        file_array = []
        # Iedere file analyseren
        # Alle bekende files wegschrijven naar file_array
        # Wanneeer deze onbekend is de file name gebruiken als extentie

        Debugger('Finding Filetypes for selected partition')
        for file in files:
            type = FileType(file).analyse()
            if type[1] is not '':
                type.append(file.name)
                file_array.append(type)

        input = self.UserInput(['Print Filetypes', 'Export Filetypes (CSV)'])
        if input == 0:
            Debugger('Printing info to console')
            # Printen mooie tabel
            print tabulate(file_array, headers=[
                           'Extention', 'Description', 'Filename'])

        else:
            Debugger('Storing results in .csv')

            # data wegschrijven naar .csv
            self.save_array_to_csv(
                file_array, 'Extention;Description;FileName')

    def cli(self):
        '''
        CommandLineInterface Vanuit hier wordt de module aangestuurd
        :return: None
        '''
        while True:
            Debugger('Bestand Hoofdmenu')

            try:
                print "\t[1] Generate Hashlist"
                print '\t[2] List ZIP/Archives'
                print '\t[3] Generate Timeline'
                print '\t[4] List Filetypes'
                print '\t[5] Find Used Languages'
                print '\t[6] Export File'
                print '\t[7] VirusTotal'
                print '\t[0] Back'
                print ''

                # Gebruikersinput uitlezen
                input = int(raw_input('Please choose an option [0-9]: '))
                Debugger('Selected option: ' + str(input))
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
                if input == 0:
                    break
            except:
                ErrorLogger()

    def virustotal_file(self):
        '''
        Bestand door virustotal halen
        :return: None
        '''
        try:
            Debugger('Virustotal')
            # Gebruiker een bestand laten selecteren
            file = self.select_file()
            # Virustotal class gebruiken
            Logger('Hash Opzoeken in virustotal')
            total = VirusTotal(file).lookup_hash()
        except:
            ErrorLogger(True)

    def export_file(self):
        '''
        Geselecteerd bestand exporteren
        :return: None
        '''
        Debugger('Bestand Exporteren')
        self.select_file().export()

    def run(self):
        '''
        Starten van Bestand's module
        :return: None
        '''
        # Wanneer er geen bruikbare images zijn terugkeren naar hoofdmenu
        if len(self.main.images) == 0:
            print "*** Please import an image before using this module! ***"
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
