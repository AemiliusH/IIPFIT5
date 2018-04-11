from datetime import *
from tabulate import tabulate
from Database import *
from time import gmtime, strftime


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Logger():
    def __init__(self, bericht, console=True):
        db = Database(None)
        db.write_log(bericht)


class Debugger():
    def __init__(self, bericht, console=False):
        db = Database(None)
        db.write_log(str('[Debug] ' + bericht))
        if console:
            print str(self.timestamp() + Debug + bericht)

    def timestamp(self):
        return str('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']')


class Reporter():
    def __init__(self, title, bericht, console=True):
        db = Database(None)
        db.write_rapportage(title, bericht)
        if console:
            print str(self.timestamp() + '[' + title + ']' + bericht)

    def timestamp(self):
        return str('[' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ']')
