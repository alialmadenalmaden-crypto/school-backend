with open(r"C:\Users\alial\super_admin_desktop\lib\pages\dashboard\sections\institutes_list_section.dart", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split('\n')
for i, line in enumerate(lines):
    if "getFormattedImageUrl" in line:
        print(f"Line {i+1}: {line.strip()}")
