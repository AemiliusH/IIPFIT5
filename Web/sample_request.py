import requests

url = 'http://127.0.0.1:5002/main?command=image'

data = {'path': 'C:\\Users\\0x000000\\Documents\\School\\Hogeschool Leiden\\Jaar 2\\IPFJURI\\Bewijs\\ZwarteSDuitKleinedrone.E01'}

resp = requests.post(url, json=data)
print resp.text
