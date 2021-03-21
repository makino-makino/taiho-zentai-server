import requests
import base64
import json

TO_URL = "http://localhost:5000"


with open('murai.jpg', 'rb') as f:
    data = f.read()

unchi = base64.b64encode(data).decode(encoding='utf-8')
#print(unchi)

response = requests.post(
    'http://127.0.0.1:5000/',
    data=json.dumps({
        'img': unchi
    }),
    headers={
        'Content-Type': 'application/json'
    })

print(response.text)
