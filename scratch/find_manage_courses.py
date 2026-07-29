with open(r"C:\Users\alial\institute_desktop\lib\pages\courses\manage_courses_page.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "DropdownButtonFormField" in line or "showAdd" in line or "dialog" in line or "Category" in line:
        if i > 5:
            print(f"Line {i+1}: {line.strip()}")
