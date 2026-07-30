with open(r"C:\Users\alial\student\lib\pages\home\booking_page.dart", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split('\n')
for i, line in enumerate(lines):
    if "_buildTextField" in line:
        print(f"Line {i+1}: {line.strip()}")
