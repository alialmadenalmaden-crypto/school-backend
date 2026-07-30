import urllib.request
import json

url = "https://education-api-ol58.onrender.com/api/courses/some-fake-id/"
data = {
    "title": "Test Title",
    "price": 50.0,
    "category_name": "اللغات - اللغة التركية",
    "period": "morning"
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='PUT'
)

try:
    urllib.request.urlopen(req)
except urllib.error.HTTPError as e:
    print(f"Status Code: {e.code}")
    print(f"Response: {e.read().decode('utf-8')}")
except Exception as ex:
    print(f"Error: {ex}")
