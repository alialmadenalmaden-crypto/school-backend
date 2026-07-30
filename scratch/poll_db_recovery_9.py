import urllib.request
import json
import time

url = "https://education-api-ol58.onrender.com/api/get-otp?email=alialmadenalmaden@gmail.com"

print("Waiting for server to deploy and fetching OTP...")
max_retries = 30
for i in range(max_retries):
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        if "code" in data:
            print(f"\nSUCCESS! OTP FOR alialmadenalmaden@gmail.com IS: {data['code']}")
            break
        else:
            print(f"Server is online but no OTP yet: {data}")
            break
    except Exception as ex:
        print(f"Waiting for server... ({i+1}/{max_retries})")
    time.sleep(10)
