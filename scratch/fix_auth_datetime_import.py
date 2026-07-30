import re

file_path = r"C:\Users\alial\student\backend\app\routers\auth.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add from datetime import datetime at the top
content = "from datetime import datetime\n" + content

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("auth.py updated with from datetime import datetime import successfully!")
