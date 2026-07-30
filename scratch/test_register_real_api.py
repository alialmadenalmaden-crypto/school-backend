import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

url = "https://education-api-ol58.onrender.com/api/auth/register"
data = {
    "full_name": "تبت نينس نينن ينيني",
    "email": "alialmadenalmaden@gmail.com",
    "phone": "73466461313"
}
data_encoded = json.dumps(data).encode("utf-8")

req = urllib.request.Request(url, data=data_encoded, method="POST")
req.add_header("Content-Type", "application/json")

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
