import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

url = "https://education-api-ol58.onrender.com/api/auth/verify-email?email=alialmadenalmaden@gmail.com&code=123456"
req = urllib.request.Request(url, data=b"", method="POST")

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.getcode()}")
        print(response.read().decode('utf-8'))
except Exception as e:
    if hasattr(e, 'read'):
        print(f"Error Code: {e.code}")
        print(e.read().decode('utf-8'))
    else:
        print(f"Error: {e}")
