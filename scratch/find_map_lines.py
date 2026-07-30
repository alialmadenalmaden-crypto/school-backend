with open(r"C:\Users\alial\institute_desktop\lib\pages\courses\manage_courses_page.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "allowedCategories.map" in line or "allowedMainCats.map" in line:
        print(f"Line {i+1}: {line.strip()}")
