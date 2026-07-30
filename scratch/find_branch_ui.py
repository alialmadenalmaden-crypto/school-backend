import os

search_dir = r"C:\Users\alial\institute_desktop\lib"
print(f"Searching in {search_dir}")

for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith('.dart'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if "branch" in content.lower() or "location" in content.lower() or "latitude" in content.lower():
                        print(f"Found in {file} (Path: {os.path.relpath(path, search_dir)})")
            except Exception:
                pass
