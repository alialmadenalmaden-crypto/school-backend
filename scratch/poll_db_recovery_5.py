import urllib.request
import urllib.parse
import json
import time

url = "https://education-api-ol58.onrender.com/api/admin/delete-student-by-email"
params = urllib.parse.urlencode({"email": "alialmadenalmaden@gmail.com"}).encode("utf-8")

req = urllib.request.Request(url, data=params, method="POST")
req.add_header("Content-Type", "application/x-www-form-urlencoded")

print("Waiting for server to deploy and deleting student email...")
max_retries = 30
for i in range(max_retries):
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print("\nEMAIL CLEARED RESULT:")
            print(json.dumps(data, indent=4, ensure_ascii=False))
            break
    except Exception as ex:
        print(f"Waiting for server... ({i+1}/{max_retries})")
    time.sleep(10)
