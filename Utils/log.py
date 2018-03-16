import time
from datetime import *
from tabulate import tabulate


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class DebugLog():
    def __init__(self, tekst):
        #timestamp = '{}-{}-{} {}:{}:{}'.format(date.year, date.month, date.day, time.hour, time.minute, time.second)
        print bcolors.WARNING + "[_] " + str(tekst) + bcolors.ENDC


class ReportLog():
    def __init__(self, tekst):
        print "[Rapportage]  " + str(tekst)
