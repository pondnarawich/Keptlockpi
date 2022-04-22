import requests
import json

url = 'http://0.0.0.0:8000/keptlock/locker/unlock/validate/pin/9f45f467-8ded-4316-8229-3f0d311269ec'
code = {'code': 482318}
r = requests.get(url, data=code)
print(r.json()['slot'])