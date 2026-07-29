import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\alial\super_admin_desktop\lib\pages\dashboard\dialogs\institute_dialogs.dart", "r", encoding="utf-8") as f:
    content = f.read()

for line in content.split('\n'):
    if "category" in line or "Checkbox" in line or "check" in line or "updateInstitute" in line:
        if len(line.strip()) < 150:
            print(line.strip())
