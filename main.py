import os
import base64
import time
import json
import requests
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

PUBLIC_KEY = os.getenv("PUBLIC_KEY")
SECRET_KEY_base64 = os.getenv("SECRET_KEY")
private_key_bytes = base64.urlsafe_b64decode(SECRET_KEY_base64)
#private_key_bytes = base64.b64decode(SECRET_KEY_base64)
print(len(private_key_bytes))

if len(private_key_bytes) == 64:
    private_key_bytes = private_key_bytes[:32]
private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)

timestamp = str(int(time.time() * 1000))

method = "POST"
base_url = "https://apiv2.nobitex.ir"
path = "/market/orders/add"
payload = {
    "type": "buy",
    "execution": "limit",
    "srcCurrency": "btc",
    "dstCurrency": "usdt",
    "amount": "0.00008", 
    "price": "64000" 
    }
body = json.dumps(payload)
body = json.dumps(payload, separators=(',', ':'))

message = (timestamp + method + path + body).encode("utf-8")

signature_bytes = private_key.sign(message)
signature = base64.b64encode(signature_bytes).decode("utf-8")
signature = base64.urlsafe_b64encode(signature_bytes).decode()

headers = {
    "Nobitex-Key": PUBLIC_KEY,
    "Nobitex-Signature": signature,
    "Nobitex-Timestamp": timestamp,
    "Content-Type": "application/json"
}

url = base_url + path
response = requests.post(url, headers=headers, data=body)
print(response.status_code)
print(response.text)
