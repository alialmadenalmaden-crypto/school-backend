import os

search_dir = r"C:\Users\alial\super_admin_desktop"
print(f"Searching in {search_dir}")

for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith('.dart'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if "instituteCategory" in content or "category" in content:
                        print(f"Found in {file}")
            except Exception:
                pass
