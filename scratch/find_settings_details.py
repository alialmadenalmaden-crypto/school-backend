import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\alial\institute_desktop\lib\pages\settings\settings_page.dart", "r", encoding="utf-8") as f:
    content = f.read()

for line in content.split('\n'):
    if "controller" in line or "TextField" in line or "Text(" in line or "save" in line.lower():
        if len(line.strip()) < 120:
            print(line.strip())
