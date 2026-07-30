import urllib.request
import time

url = "https://education-api-ol58.onrender.com/api/db-status"

print("Waiting for server to redeploy after email OTP updates...")
max_retries = 30
for i in range(max_retries):
    try:
        response = urllib.request.urlopen(url)
        print(f"Server is online with new updates! Code: {response.getcode()}")
        break
    except Exception as ex:
        print(f"Server is updating, waiting... ({i+1}/{max_retries})")
    time.sleep(10)
