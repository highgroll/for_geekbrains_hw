import requests
import json

url = 'https://api.github.com/users/highgroll/repos'

resp = requests.get(url)
data = resp.json()

with open('data_GitHub.json', 'w') as f:
    json.dump(data, f)
for el in data:
    print(el['name'])



