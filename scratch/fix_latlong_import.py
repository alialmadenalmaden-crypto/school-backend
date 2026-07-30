import re

file_path = r"C:\Users\alial\institute_desktop\lib\pages\settings\settings_page.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace latlong2.dart with latlong.dart
content = content.replace("package:latlong2/latlong2.dart", "package:latlong2/latlong.dart")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Import statement corrected to package:latlong2/latlong.dart!")
