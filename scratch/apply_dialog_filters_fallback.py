import re

file_path = r"C:\Users\alial\institute_desktop\lib\pages\courses\manage_courses_page.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the language items filter to support hasSpecificLanguages fallback
old_items_filter = """                            ...controller.languagesList.where((lang) {
                              final langName = lang['name'] ?? '';
                              // Only show languages checked for this institute (e.g. "اللغة اللغة الإنجليزية")
                              return allowedCategories.contains('اللغة ' + langName);
                            }).map((lang) {"""

new_items_filter = """                            ...controller.languagesList.where((lang) {
                              final langName = lang['name'] ?? '';
                              // If the institute has no specific language sub-checkboxes saved (e.g. just "اللغات"),
                              // we show all languages as a fallback. If they have specific languages, we filter.
                              final hasSpecificLanguages = allowedCategories.any((c) => c.startsWith('اللغة '));
                              if (!hasSpecificLanguages) {
                                return true;
                              }
                              return allowedCategories.contains('اللغة ' + langName);
                            }).map((lang) {"""

content_updated = content.replace(old_items_filter, new_items_filter)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content_updated)

print("Smart fallback filtering applied successfully!")
