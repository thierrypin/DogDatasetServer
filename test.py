# -*- coding: utf-8 -*-

import requests
import json

import base64

# msg = {"name": "tantão", "breed": "", "petType": "cat", "sex": "masc"}

with open('/home/thierry/Pictures/t.png', 'rb') as f:
    img = f.read()

imgb64 = base64.encodebytes(img).decode('ascii')

msg = {"photo": imgb64}
payload = json.dumps(msg)


response = requests.post("http://127.0.0.1:5000/newphoto/10", json=payload)

print(response.content)

