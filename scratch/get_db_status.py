import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

url = "https://education-api-ol58.onrender.com/api/db-status"

try:
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    print("TABLES:")
    print(data.get("tables"))
    print("\nUSERS:")
    print(data.get("users"))
    print("\nINSTITUTES:")
    print(data.get("institutes"))
    print("\nSTUDENTS:")
    print(data.get("students"))
except Exception as e:
    print(f"Error: {e}")
