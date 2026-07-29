import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\alial\super_admin_desktop\lib\controllers\institutes_controller.dart", "r", encoding="utf-8") as f:
    content = f.read()

for line in content.split('\n'):
    if "update" in line or "put" in line or "post" in line or "category" in line or "language" in line:
        print(line.strip())
