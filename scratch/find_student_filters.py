import os

search_dir = r"C:\Users\alial\student\lib"
print(f"Searching for filter or search related files in {search_dir}")

for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith('.dart'):
            if 'filter' in file.lower() or 'search' in file.lower() or 'location' in file.lower() or 'home' in file.lower():
                print(os.path.join(root, file))
