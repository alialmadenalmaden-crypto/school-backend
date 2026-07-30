import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\alial\super_admin_desktop\lib\pages\dashboard\dialogs\institute_dialogs.dart", "r", encoding="utf-8") as f:
    content = f.read()

for i, line in enumerate(content.split('\n')):
    if "controller" in line or "TextField" in line or "TextFormField" in line or "العنوان" in line:
        if len(line.strip()) < 120:
            print(f"Line {i+1}: {line.strip()}")
