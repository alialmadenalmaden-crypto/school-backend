import urllib.request
import time

url = "https://education-api-ol58.onrender.com/api/smtp-debug"

print("Waiting for server to deploy and apply student deletion sync changes...")
max_retries = 30
for i in range(max_retries):
    try:
        response = urllib.request.urlopen(url)
        print(f"Server is online with student deletion fixes! Code: {response.getcode()}")
        break
    except Exception as ex:
        print(f"Waiting for server... ({i+1}/{max_retries})")
    time.sleep(10)
