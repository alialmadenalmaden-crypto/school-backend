import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\alial\institute_desktop\lib\pages\settings\settings_page.dart", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split('\n')
for i, line in enumerate(lines):
    if "logo" in line.lower() or "upload" in line.lower() or "image" in line.lower():
        if len(line.strip()) < 120:
            print(f"Line {i+1}: {line.strip()}")
