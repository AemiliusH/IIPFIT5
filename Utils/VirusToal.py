import requests

from tabulate import tabulate
from Utils.log import *
# Virustotal Account
'''
hocuhunof@web2mailco.com
tes*****
'''


class VirusTotal:
    # Virustotal API Key
    api_key = 'dd7d382168ca4db749f343cfd4f491a9a0aa5d2a94f38a95793fe7f6b8ba0445'

    def __init__(self, file):
        '''
        Module voor het scannen van files op mogelijke virus infecties
        :param file: FSFileObject referentie naar te scannen bestand
        '''
        # Opslaan belangrijke parameters
        self.file_handle = file

    def lookup_hash(self):
        '''
        Bestand controleren op virussen d.m.v. hashing
        :return: None
        '''
        # Hash genereren van file
        sha256 = self.file_handle.sha256()

        Debugger(
            'Looking up SHA256 hash of file in virustotal database: ' + str(sha256))
        # API request voorbereiden
        params = {'apikey': self.api_key,
                  'resource': sha256}
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "gzip"
        }

        # request posten naar virustotal
        response = requests.post(
            'https://www.virustotal.com/vtapi/v2/file/report', params=params)

        # Response omzetten naar json
        json_response = response.json()

        # Aantal positieve resultaten tellen
        if 'positives' not in json_response:
            Logger('File has not been uploaded yet!')
            return
        positives = int(json_response['positives'])
        total = int(json_response['total'])
        positives_results = []

        Debugger('Positives: ' + str(positives))
        Debugger('Total: ' + str(total))

        # Wanneer er positieve resultaten zijn, printen
        if positives > 0:
            print 'Found ' + str(positives) + '/' + \
                str(total) + ' positive Virus Results'

            # resulten openen in nieuw json object
            objects = json_response['scans']

            # voor ieder object de details printen wanneer er een detectie is
            for key, value in objects.items():
                if objects[key]['detected']:
                    Debugger(str(key) + ' ' + str(objects[key]['result']))
                    positives_results.append([key, objects[key]['result']])

            # tabel printen
            print tabulate(positives_results, headers=['Antivirus', 'Result'])
        else:
            Logger('File is clean!')
