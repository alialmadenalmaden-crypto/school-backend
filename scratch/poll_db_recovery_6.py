import urllib.request
import json
import time

url = "https://education-api-ol58.onrender.com/api/auth/delete-student-by-email?email=alialmadenalmaden@gmail.com"

print("Waiting for server to deploy and deleting student email via auth router...")
max_retries = 30
for i in range(max_retries):
    try:
        req = urllib.request.Request(url, data=b"", method="POST")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print("\nEMAIL CLEARED RESULT:")
            print(json.dumps(data, indent=4, ensure_ascii=False))
            break
    except Exception as ex:
        print(f"Waiting for server... ({i+1}/{max_retries})")
    time.sleep(10)
