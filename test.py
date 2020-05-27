# -*- coding: utf-8 -*-

import requests
import json

msg = {"name": "tantão", "breed": "", "petType": "cat", "sex": "masc"}

payload = json.dumps(msg)

response = requests.post("http://127.0.0.1:5000/newpet", json=payload)

print(response.content)

