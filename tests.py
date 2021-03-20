import requests, base64, json

unchi = base64.b64encode(b'unchi').decode(encoding='utf-8')


response = requests.post(
    'http://127.0.0.1:5000/',
    data=json.dumps({
         'img': unchi 
    }),
    headers={
        'Content-Type': 'application/json' 
    })

print(response.text)
