import requests
import json

url = 'https://api.vk.com/method/users.get'
user_token = '009299d1d0d7b44b587ba308350e3a12c3c33f4e071b1f00faad3acd185aef242c6dc5cbedcd93df0a387'
parameters = {'v': '5.52',
              'access_token': user_token}
resp = requests.get(url, params=parameters)
data = resp.json()
with open('data_VK.json', 'w') as f:
    json.dump(data, f)
