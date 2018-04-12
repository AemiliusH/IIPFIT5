import traceback
import sys
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


class ErrorLogger:
    def __init__(self, console=False):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        trace = traceback.extract_tb(exc_traceback)[0]

        error = []
        error.append(['Type', str(exc_type)])
        error.append(['File', str(trace[0])])
        error.append(['Message', str(exc_value)])
        error.append(['Line', str(trace[1])])
        error.append(['Function', str(trace[2])])

        error = tabulate(error, headers=['Type', 'value'])

        db = Database(None)
        db.write_error(error)
        if console:
            print self.timestamp(), 'An error occured!'
            print error

    def timestamp(self):
        '''
        Getting current timestamp as string
        :return: Timestamp as formatted string
        '''
        return str('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']')

class Logger:
    def __init__(self, bericht, console=True):
        '''
        Logger thats writing to console by default
        :param bericht: Text input
        :param console: Boolean default true
        '''
        db = Database(None)
        db.write_log(bericht)
        if console:
            print self.timestamp(), bericht

    def timestamp(self):
        '''
        Getting current timestamp as string
        :return: Timestamp as formatted string
        '''
        return str('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']')


class Debugger():
    def __init__(self, bericht, console=False):
        db = Database(None)
        db.write_log(str('[Debug] ' + bericht))
        if console:
            print str(self.timestamp() + bericht)

    def timestamp(self):
        '''
        Getting current timestamp as string
        :return: Timestamp as formatted string
        '''
        return str('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']')


class Reporter():
    def __init__(self, title, bericht, console=True):
        db = Database(None)
        db.write_rapportage(title, bericht)
        if console:
            print str(self.timestamp() + '[' + title + ']' + bericht)

    def timestamp(self):
        return str('[' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ']')
