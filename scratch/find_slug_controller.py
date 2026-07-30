with open(r"C:\Users\alial\institute_desktop\lib\pages\auth\login_page.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "_slugController" in line:
        print(f"Line {i+1}: {line.strip()}")
