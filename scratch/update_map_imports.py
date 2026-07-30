import re

file_path = r"C:\Users\alial\institute_desktop\lib\pages\settings\settings_page.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Make sure we don't have duplicate imports
content = content.replace("import 'package:latlong2/latlong2.dart';\n", "")

# Add imports
content = "import 'package:flutter_map/flutter_map.dart';\nimport 'package:latlong2/latlong2.dart';\n" + content

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Map imports added to settings page!")
