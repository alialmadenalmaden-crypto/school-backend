import os

files = [
    r"C:\Users\alial\super_admin_desktop\lib\pages\dashboard\sections\institutes_list_section.dart",
    r"C:\Users\alial\super_admin_desktop\lib\pages\dashboard\dialogs\institute_dialogs.dart",
]

for fp in files:
    print(f"File: {fp}")
    with open(fp, "r", encoding="utf-8", errors='ignore') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if "getFormattedImageUrl" in line:
            # print surrounding lines
            start = max(0, i-5)
            end = min(len(lines), i+15)
            print(f"--- line {i+1} ---")
            for j in range(start, end):
                print(f"{j+1}: {lines[j].strip()}")
