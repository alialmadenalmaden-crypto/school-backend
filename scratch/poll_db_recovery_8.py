import urllib.request
import json
import time

url = "https://education-api-ol58.onrender.com/api/auth/delete-student-by-email?email=alialmadenalmaden@gmail.com"
url2 = "https://education-api-ol58.onrender.com/api/auth/delete-student-by-email?email=alimaen737@gmail.com"

print("Waiting for server to deploy and apply background email task changes...")
max_retries = 30
for i in range(max_retries):
    try:
        req = urllib.request.Request(url, data=b"", method="POST")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print("\nEMAIL alialmadenalmaden@gmail.com CLEARED RESULT:")
            print(json.dumps(data, indent=4, ensure_ascii=False))
            
        req2 = urllib.request.Request(url2, data=b"", method="POST")
        with urllib.request.urlopen(req2) as response2:
            data2 = json.loads(response2.read().decode('utf-8'))
            print("EMAIL alimaen737@gmail.com CLEARED RESULT:")
            print(json.dumps(data2, indent=4, ensure_ascii=False))
            break
    except Exception as ex:
        print(f"Waiting for server... ({i+1}/{max_retries})")
    time.sleep(10)
