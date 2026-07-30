import os

parent_dir = r"C:\Users\alial"
dirs = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]
print("Directories in C:\\Users\\alial:")
for d in dirs:
    if 'admin' in d.lower() or 'desktop' in d.lower():
        print(d)
