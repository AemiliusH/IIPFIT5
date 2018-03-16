import requests

from tabulate import tabulate

'''
hocuhunof@web2mailco.com
test1234
'''


class VirusTotal:

    api_key = 'dd7d382168ca4db749f343cfd4f491a9a0aa5d2a94f38a95793fe7f6b8ba0445'

    def __init__(self, file):
        self.file_handle = file

    def lookup_hash(self):
        sha256 = self.file_handle.sha256()
        params = {'apikey': self.api_key,
                  'resource': 'fcc1bd24951b5dca31147bbc33d3566c23fb1a78a9afcbb62d0ae9e7695517ed'}
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "gzip"
        }
        response = requests.post(
            'https://www.virustotal.com/vtapi/v2/file/report', params=params)
        json_response = response.json()

        positives = int(json_response['positives'])
        total = int(json_response['total'])
        positives_results = []
        if positives > 0:
            print 'Found ' + str(positives) + '/' + \
                str(total) + ' positive Virus Results'

            objects = json_response['scans']

            for key, value in objects.items():
                if objects[key]['detected']:
                    positives_results.append([key, objects[key]['result']])

            print tabulate(positives_results, headers=['Antivirus', 'Result'])
        else:
            print 'File is clean!'
