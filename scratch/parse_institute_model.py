import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\alial\super_admin_desktop\lib\models\institute_model.dart", "r", encoding="utf-8") as f:
    content = f.read()

for line in content.split('\n'):
    if "class" in line or "final" in line or "factory" in line or "category" in line:
        print(line.strip())
