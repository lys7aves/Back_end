import requests

url = '127.0.0.1:8000/start'
headers = {
    'X-Auth-Token: 1234',
    'Content-Type: application/json'
}
data = {
    "problem": 1
}

r = requests(url, headers=headers, data=data)