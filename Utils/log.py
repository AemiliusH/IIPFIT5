import time 
from datetime import * 
from tabulate import tabulate

class DebugLog():
    def __init__(self,tekst): 
        #timestamp = '{}-{}-{} {}:{}:{}'.format(date.year, date.month, date.day, time.hour, time.minute, time.second)
        print "[_] " + str(tekst)

class ReportLog():
    def __init__(self, tekst): 
        print "[Rapportage]  " + str(tekst)