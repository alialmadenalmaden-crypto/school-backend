import urllib.request
import json
import time

url = "https://education-api-ol58.onrender.com/api/smtp-debug"

print("Waiting for server to deploy and querying smtp-debug endpoint...")
max_retries = 30
for i in range(max_retries):
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        print("\nSMTP CONFIG ON SERVER:")
        print(json.dumps(data, indent=4, ensure_ascii=False))
        break
    except Exception as ex:
        print(f"Waiting for server to reboot... ({i+1}/{max_retries})")
    time.sleep(10)
