import urllib.request
import time
import json

url = "https://education-api-ol58.onrender.com/api/admin/clear-dummy-data"

print("Waiting for server to redeploy and update database tables...")
max_retries = 30
for i in range(max_retries):
    try:
        req = urllib.request.Request(url, method='POST')
        response = urllib.request.urlopen(req)
        body = response.read().decode('utf-8')
        print(f"Server response code: {response.getcode()}")
        print(f"Response: {body}")
        break
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Server is online but endpoint not ready yet (404). Retrying in 10 seconds... ({i+1}/{max_retries})")
        else:
            print(f"Error {e.code}: {e.read().decode('utf-8')}")
            break
    except Exception as ex:
        print(f"Waiting for server to wake up... ({i+1}/{max_retries})")
    time.sleep(10)
