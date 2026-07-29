import os

search_dir = r"C:\Users\alial\.gemini\antigravity\brain\6e9527b4-322f-47f1-9805-6b095c816c20"
print(f"Searching for 'postgres' connection string in: {search_dir}")

found = False
for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith(('.json', '.py', '.txt', '.log', '.jsonl')):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if "postgresql://" in content:
                        for line in content.split('\n'):
                            if "postgresql://" in line and "localhost" not in line:
                                print(f"Found in {file}: {line.strip()}")
                                found = True
            except Exception:
                pass

if not found:
    print("No remote postgres url found in logs.")
