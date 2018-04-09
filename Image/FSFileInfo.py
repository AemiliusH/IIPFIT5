import hashlib
import re

from langdetect import detect_langs
from shutil import copyfileobj
from StringIO import StringIO
from Utils.log import *
from Utils.FileType import *


class FSFileInfo():
    # Initaliseren van class variable
    size = 0
    name = ''
    extention = ''

    def __init__(self, object_handle, path):
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

    # Geeft een lijst terug met alle beschikbare meta-data van bestand
    # Zeer bruikbaar om tabellen te genereren
    def get_attributes(self):
        return [self.name, self.size, self.create, self.change, self.modify, self.md5(), self.sha256()]

    # Exporteert een bestand vanuit image naar fysieke schijf
    def export(self):
        # Uitlezen bytes van bestand
        raw_bytes = StringIO(self.object_handle.read_random(0, self.size))
        # Referentie openen naar export bestand op schijf
        # Naam van orginele file wordt gebruikt in uitvoer map
        file = open(self.name, 'w')
        # Byte focus bij eerste byte leggen (vanaaf hier wordt niet uit gelezen)
        raw_bytes.seek(0)
        # Verplaatsen van bytes naar bestands referentie
        copyfileobj(raw_bytes, file)

    # Header of file
    def head(self, size=4):
        # Leest eerste 4 bytes van file uit
        try:
            return self.object_handle.read_random(0, size)
        except:
            return ''

    def get_extention(self):
        # Gebruikt FileType class om extentie van bestand te analyseren
        return FileType(self).analyse()

    def read_raw_bytes(self):
        try:
            # Lezen van raw bytes in try / except
            return self.object_handle.read_random(0, self.size)
        except IOError:
            return ''

    # Uitlezen van alle woorden in bestand
    def get_strings(self):
        # Alle woorden uit bestand krijgen d.m.v. Regulair Expressions
        words = re.findall('[aA-zZ]+', self.read_raw_bytes())
        # Woorden filteren die langer zijn dan 4 karakters
        return [w for w in words if len(w) >= 4]

    def detect_language(self):
        # Omzetten van woordarray naar tekst
        text = ' '.join(self.get_strings())
        # Google's langdetect gebruiken om de taal van een bestand te achterhalen.
        return detect_langs(text)

    def print_language_table(self):
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
        # Inladen van libhash's functie md5()
        libhash = hashlib.md5()
        # Bytes van bestand meegeven aan libhash
        libhash.update(self.read_raw_bytes())
        # Returning de hexadecimale vorm van de hash
        return libhash.hexdigest()

    def sha1(self):
        # Inladen van libhash's functie Sha1()
        libhash = hashlib.sha1()
        # Bytes van bestand meegeven aan libhash
        libhash.update(self.read_raw_bytes())
        # Returning de hexadecimale vorm van de hash
        return libhash.hexdigest()

    def sha256(self):
        # Inladen van libhash's functie Sha256()
        libhash = hashlib.sha256()
        # Bytes van bestand meegeven aan libhash
        libhash.update(self.read_raw_bytes())
        # Returning de hexadecimale vorm van de hash
        return libhash.hexdigest()
