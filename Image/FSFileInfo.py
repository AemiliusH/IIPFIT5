import hashlib
import re

from langdetect import detect_langs
from shutil import copyfileobj
from StringIO import StringIO
from Utils.log import *
from Utils.FileType import *
from Utils.Database import *


class FSFileInfo():
    # Initaliseren van class variable
    size = 0
    name = ''
    extention = ''

    def __init__(self, object_handle, path):
        '''
        Bevat file informatie en benodigde functionaliteiten om bestanden te kunnen verwerken
        :param object_handle: Pointer naar fsobject
        :param path: Path van bestand
        '''
        # Opslaan van belangrijke parameters
        self.path = path
        self.object_handle = object_handle

        # Het invullen van de file eigenschappen
        self.size = self.object_handle.info.meta.size
        self.name = object_handle.info.name.name

        # Berekenen van meta-data gegevens
        # Timestamp wordt omgezet naar bruikbaar datatype
        self.create = datetime.utcfromtimestamp(
            self.object_handle.info.meta.crtime)
        self.change = datetime.utcfromtimestamp(
            self.object_handle.info.meta.ctime)
        self.modify = datetime.utcfromtimestamp(
            self.object_handle.info.meta.mtime)

    def get_attributes(self):
        Debugger('Getting Attributes for ' +
                 str(self.name))
        '''
        Geeft een lijst terug met alle beschikbare meta-data van bestand
        Zeer bruikbaar om tabellen te genereren
        :return: Arraylist met alle meta-data
        '''
        return [self.name, self.size, self.create, self.change, self.modify, self.md5(), self.sha256()]

    def export(self):
        '''
        Exporteert een bestand vanuit image naar fysieke schijf
        :return: None
        '''

        Debugger('Exporting file:  ' + str(self.name))

        # Uitlezen bytes van bestand
        raw_bytes = StringIO(self.object_handle.read_random(0, self.size))
        # Referentie openen naar export bestand op schijf
        # Naam van orginele file wordt gebruikt in uitvoer map
        file = open(self.name, 'w')
        # Byte focus bij eerste byte leggen (vanaaf hier wordt niet uit gelezen)
        raw_bytes.seek(0)
        # Verplaatsen van bytes naar bestands referentie
        copyfileobj(raw_bytes, file)

    def head(self, size=4):
        '''
        Verkrijg Header van file
        :param size: Grootte van header (standaard 4)
        :return: Bytes
        '''

        Debugger('Getting Header bytes for ' +
                 str(self.name))

        # Leest eerste 4 bytes van file uit
        try:
            return self.object_handle.read_random(0, size)
        except:
            return ''

    def get_extention(self):

        Debugger('Getting Extention for ' +
                 str(self.name))

        '''
        Verkrijgen van extentie informatie vanuit FileType class
        :return: FileType analyse object
        '''
        # Gebruikt FileType class om extentie van bestand te analyseren
        return FileType(self).analyse()

    def read_raw_bytes(self):
        '''
        Lezen van bytes in try / except
        :return: Alle bytes van file
        '''
        Debugger('Reading bytes from ' +
                 str(self.name))

        try:
            # Lezen van raw bytes in try / except
            return self.object_handle.read_random(0, self.size)
        except IOError:
            return ''

    def get_strings(self):
        '''
        Uitlezen van alle woorden in bestand
        Waarvan de lengte 4 of langer is
        :return: arraylist met alle woorden in bestand
        '''

        Debugger('Getting all strings from' +
                 str(self.name))
        # Alle woorden uit bestand krijgen d.m.v. Regulair Expressions
        words = re.findall('[aA-zZ]+', self.read_raw_bytes())
        # Woorden filteren die langer zijn dan 4 karakters
        return [w for w in words if len(w) >= 4]

    def detect_language(self):
        '''
        Detecteren van taal waarin een besatnd is geschreven
        :return: detect_langs array
        '''
        Debugger('Detecting Language for ' +
                 str(self.name))
        # Omzetten van woordarray naar tekst
        text = ' '.join(self.get_strings())
        # Google's langdetect gebruiken om de taal van een bestand te achterhalen.
        return detect_langs(text)

    def print_language_table(self):
        '''
        Print een tabel van alle talen gebruikt in file
        :return: None
        '''

        # Getting all Languages from File
        languages = self.detect_language()
        language_array = []
        for lang in languages:
            # Converting them into a new array
            language_array.append(str(lang).split(':'))
        # Printing Array as Table
        print tabulate(language_array, headers=['Language', '.%'])

    # Objecten hashen
    def md5(self):
        '''
        Bereken MD5 van bestand
        :return: MD5 Hash
        '''

        # Inladen van libhash's functie md5()
        libhash = hashlib.md5()
        # Bytes van bestand meegeven aan libhash
        libhash.update(self.read_raw_bytes())
        # Returning de hexadecimale vorm van de hash
        return libhash.hexdigest()

    def sha1(self):
        '''
        Berekend SHA1 van bestand
        :return: SHA1 Hash
        '''
        # Inladen van libhash's functie Sha1()
        libhash = hashlib.sha1()
        # Bytes van bestand meegeven aan libhash
        libhash.update(self.read_raw_bytes())
        # Returning de hexadecimale vorm van de hash
        return libhash.hexdigest()

    def sha256(self):
        '''
        Bereken SHA256 van bestand
        :return: SHA256 Hash
        '''
        # Inladen van libhash's functie Sha256()
        libhash = hashlib.sha256()
        # Bytes van bestand meegeven aan libhash
        libhash.update(self.read_raw_bytes())
        # Returning de hexadecimale vorm van de hash
        return libhash.hexdigest()
