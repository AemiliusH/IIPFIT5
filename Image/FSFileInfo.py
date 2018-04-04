import hashlib
import re

from langdetect import detect_langs
from shutil import copyfileobj
from StringIO import StringIO
from Utils.log import *
from Utils.FileType import *


class FSFileInfo():
    size = 0
    name = ''
    extention = ''

    def __init__(self, object_handle, path):
        self.path = path
        self.object_handle = object_handle
        self.size = self.object_handle.info.meta.size
        self.name = object_handle.info.name.name
        self.create = datetime.utcfromtimestamp(
            self.object_handle.info.meta.crtime)
        self.change = datetime.utcfromtimestamp(
            self.object_handle.info.meta.ctime)
        self.modify = datetime.utcfromtimestamp(
            self.object_handle.info.meta.mtime)

    def get_attributes(self):
        return [self.name, self.size, self.create, self.change, self.modify, self.md5(), self.sha256()]

    def export(self):
        raw_bytes = StringIO(self.object_handle.read_random(0, self.size))
        file = open(self.name, 'w')
        raw_bytes.seek(0)
        copyfileobj(raw_bytes, file)

    def export_to(self):
        raw_bytes = StringIO(self.object_handle.read_random(0, self.size))
        file = open("DataBase\\" + self.name, 'w')
        raw_bytes.seek(0)
        copyfileobj(raw_bytes, file)

    # Header of file
    def head(self, size=4):
        try:
            return self.object_handle.read_random(0, size)
        except:
            return ''

    def get_extention(self):
        return FileType(self).analyse()

    def read_raw_bytes(self):
        try:
            return self.object_handle.read_random(0, self.size)
        except IOError:
            return ''

    def get_strings(self):
        # Getting all Words from file
        words = re.findall('[aA-zZ]+', self.read_raw_bytes())
        # Filtering Words for 4 characters or longer
        return [w for w in words if len(w) >= 4]

    def detect_language(self):
        # Converting wordarray to string
        text = ' '.join(self.get_strings())
        # Using Google's langdetect to detect used file language
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

    # Hashing Objects
    def md5(self):
        libhash = hashlib.md5()
        libhash.update(self.read_raw_bytes())
        return libhash.hexdigest()

    def sha1(self):
        libhash = hashlib.sha1()
        libhash.update(self.read_raw_bytes())
        return libhash.hexdigest()

    def sha256(self):
        libhash = hashlib.sha256()
        libhash.update(self.read_raw_bytes())
        return libhash.hexdigest()
