import re

file_path = r"C:\Users\alial\institute_desktop\lib\pages\courses\manage_courses_page.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace category parse in _showAddCourseDialog
old_cats_parse_add = """    final authController = Get.find<AuthController>();
    final rawCats = authController.instituteCategory.value;
    final allowedCategories = rawCats.isNotEmpty
        ? rawCats.split(',').map((c) => c.trim()).where((c) => c.isNotEmpty).toList()
        : <String>[];
    if (allowedCategories.isEmpty) {
      allowedCategories.addAll(['اللغات - إنجليزية', 'الحاسوب']);
    }
    String selectedCategory = allowedCategories.first;"""

new_cats_parse_add = """    final authController = Get.find<AuthController>();
    final rawCats = authController.instituteCategory.value;
    final allowedCategories = rawCats.isNotEmpty
        ? rawCats.split(',').map((c) => c.trim()).where((c) => c.isNotEmpty).toList()
        : <String>[];
    
    final mainDepartments = ['اللغات', 'الحاسوب', 'التقوية الدراسي', 'المعاهد الطبية', 'المعاهد المهنية'];
    final allowedMainCats = allowedCategories.where((c) => mainDepartments.contains(c)).toList();
    if (allowedMainCats.isEmpty) {
      allowedMainCats.addAll(['اللغات', 'الحاسوب']);
    }
    String selectedCategory = allowedMainCats.first;"""

content_updated = content.replace(old_cats_parse_add, new_cats_parse_add)

# Replace category parse in _showEditCourseDialog
old_cats_parse_edit = """    final authController = Get.find<AuthController>();
    final rawCats = authController.instituteCategory.value;
    final allowedCategories = rawCats.isNotEmpty
        ? rawCats.split(',').map((c) => c.trim()).where((c) => c.isNotEmpty).toList()
        : <String>[];
    if (allowedCategories.isEmpty) {
      allowedCategories.addAll(['اللغات - إنجليزية', 'الحاسوب']);
    }
    String selectedCategory = allowedCategories.contains(course.categoryName)
        ? course.categoryName
        : allowedCategories.first;"""

new_cats_parse_edit = """    final authController = Get.find<AuthController>();
    final rawCats = authController.instituteCategory.value;
    final allowedCategories = rawCats.isNotEmpty
        ? rawCats.split(',').map((c) => c.trim()).where((c) => c.isNotEmpty).toList()
        : <String>[];
    
    final mainDepartments = ['اللغات', 'الحاسوب', 'التقوية الدراسي', 'المعاهد الطبية', 'المعاهد المهنية'];
    final allowedMainCats = allowedCategories.where((c) => mainDepartments.contains(c)).toList();
    if (allowedMainCats.isEmpty) {
      allowedMainCats.addAll(['اللغات', 'الحاسوب']);
    }
    String selectedCategory = allowedMainCats.contains(course.categoryName)
        ? course.categoryName
        : allowedMainCats.first;"""

content_updated = content_updated.replace(old_cats_parse_edit, new_cats_parse_edit)

# Update allowedCategories to allowedMainCats in dropdown items mapping in add course dialog
content_updated = content_updated.replace(
    "items: allowedCategories.map((cat) {",
    "items: allowedMainCats.map((cat) {"
)

# Update allowedCategories filter for language dropdown in both dialogs
old_lang_dropdown = """                        // Language Dropdown
                        DropdownButtonFormField<String>(
                          value: selectedLanguageId,
                          dropdownColor: cardColor,
                          style: TextStyle(color: textColor, fontSize: 13),
                          decoration: InputDecoration(
                            labelText: 'اللغة المستهدفة (اختياري)',
                            labelStyle: TextStyle(color: subTextColor),
                            filled: true,
                            fillColor: fieldBg,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            prefixIcon: const Icon(Icons.translate_rounded, color: AppColors.primary),
                          ),
                          items: [
                            const DropdownMenuItem<String>(
                              value: null,
                              child: Text('بدون لغة محددة', style: TextStyle(color: Colors.grey)),
                            ),
                            ...controller.languagesList.map((lang) {
                              return DropdownMenuItem<String>(
                                value: lang['id'],
                                child: Text(lang['name'] ?? '', style: TextStyle(color: textColor)),
                              );
                            }).toList(),
                          ],
                          onChanged: (val) {
                            setState(() {
                              selectedLanguageId = val;
                            });
                          },
                        ),"""

new_lang_dropdown = """                        // Language Dropdown (Filtered by allowed languages for this institute)
                        DropdownButtonFormField<String>(
                          value: selectedLanguageId,
                          dropdownColor: cardColor,
                          style: TextStyle(color: textColor, fontSize: 13),
                          decoration: InputDecoration(
                            labelText: 'اللغة المستهدفة (اختياري)',
                            labelStyle: TextStyle(color: subTextColor),
                            filled: true,
                            fillColor: fieldBg,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            prefixIcon: const Icon(Icons.translate_rounded, color: AppColors.primary),
                          ),
                          items: [
                            const DropdownMenuItem<String>(
                              value: null,
                              child: Text('بدون لغة محددة', style: TextStyle(color: Colors.grey)),
                            ),
                            ...controller.languagesList.where((lang) {
                              final langName = lang['name'] ?? '';
                              // Only show languages checked for this institute (e.g. "اللغة اللغة الإنجليزية")
                              return allowedCategories.contains('اللغة ' + langName);
                            }).map((lang) {
                              return DropdownMenuItem<String>(
                                value: lang['id'],
                                child: Text(lang['name'] ?? '', style: TextStyle(color: textColor)),
                              );
                            }).toList(),
                          ],
                          onChanged: (val) {
                            setState(() {
                              selectedLanguageId = val;
                            });
                          },
                        ),"""

# Perform replacement for lang dropdown (allow multiple replacements for add and edit dialogs)
content_updated = content_updated.replace(old_lang_dropdown, new_lang_dropdown)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content_updated)

print("Filtering applied successfully!")
