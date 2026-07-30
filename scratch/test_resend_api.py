import urllib.request
import urllib.parse
import json

url = "https://education-api-ol58.onrender.com/api/auth/resend-code"
params = urllib.parse.urlencode({"email": "alialmaden.almaden@gmail.com"}).encode("utf-8")

req = urllib.request.Request(url, data=params, method="POST")
req.add_header("Content-Type", "application/x-www-form-urlencoded")

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
