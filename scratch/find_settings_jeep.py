with open(r"C:\Users\alial\institute_desktop\lib\pages\settings\settings_page.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "_jeepNumberController" in line:
        print(f"Line {i+1}: {line.strip()}")
