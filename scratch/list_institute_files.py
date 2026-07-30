import os

search_dir = r"C:\Users\alial\institute_desktop\lib"
for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith('.dart'):
            rel_path = os.path.relpath(os.path.join(root, file), search_dir)
            print(rel_path)
