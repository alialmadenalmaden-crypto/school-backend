import urllib.request
import json
import time

url = "https://education-api-ol58.onrender.com/api/smtp-debug"

print("Waiting for server to rebuild and deploy with Resend configuration...")
max_retries = 30
for i in range(max_retries):
    try:
        response = urllib.request.urlopen(url)
        print(f"Server is online! Code: {response.getcode()}")
        break
    except Exception as ex:
        print(f"Waiting for server... ({i+1}/{max_retries})")
    time.sleep(10)
