import re

file_path = r"C:\Users\alial\institute_desktop\lib\pages\courses\manage_courses_page.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update allowedMainCats parsing in _showAddCourseDialog
old_vars_parse_add = """    final authController = Get.find<AuthController>();
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

new_vars_parse_add = """    final authController = Get.find<AuthController>();
    final rawCats = authController.instituteCategory.value;
    final allowedMainCats = rawCats.isNotEmpty
        ? rawCats.split(',').map((c) => c.trim()).where((c) => c.isNotEmpty).toList()
        : <String>[];
    if (allowedMainCats.isEmpty) {
      allowedMainCats.addAll(['اللغات', 'الحاسوب']);
    }
    final allowedCategories = List<String>.from(allowedMainCats);
    String selectedCategory = allowedMainCats.first;"""

content = content.replace(old_vars_parse_add, new_vars_parse_add)

# 2. Update allowedMainCats parsing in _showEditCourseDialog
old_vars_parse_edit = """    final authController = Get.find<AuthController>();
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

new_vars_parse_edit = """    final authController = Get.find<AuthController>();
    final rawCats = authController.instituteCategory.value;
    final allowedMainCats = rawCats.isNotEmpty
        ? rawCats.split(',').map((c) => c.trim()).where((c) => c.isNotEmpty).toList()
        : <String>[];
    if (allowedMainCats.isEmpty) {
      allowedMainCats.addAll(['اللغات', 'الحاسوب']);
    }
    final allowedCategories = List<String>.from(allowedMainCats);
    String selectedCategory = allowedMainCats.contains(course.categoryName)
        ? course.categoryName
        : allowedMainCats.first;"""

content = content.replace(old_vars_parse_edit, new_vars_parse_edit)


# 3. Period selector widget in Add Dialog
old_period_dropdown_add = """                        // Period Selection Dropdown (Morning / Evening)
                        DropdownButtonFormField<String>(
                          value: selectedPeriod,
                          dropdownColor: cardColor,
                          style: TextStyle(color: textColor, fontSize: 13),
                          decoration: InputDecoration(
                            labelText: 'الفترة الدراسية للكورس',
                            labelStyle: TextStyle(color: subTextColor),
                            filled: true,
                            fillColor: fieldBg,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            prefixIcon: Icon(selectedPeriod == 'morning' ? Icons.wb_sunny_rounded : Icons.nights_stay_rounded, color: AppColors.primary),
                          ),
                          items: [
                            DropdownMenuItem<String>(
                              value: 'morning',
                              child: Text('صباحي', style: TextStyle(color: textColor)),
                            ),
                            DropdownMenuItem<String>(
                              value: 'evening',
                              child: Text('مسائي', style: TextStyle(color: textColor)),
                            ),
                          ],
                          onChanged: (val) {
                            if (val != null) {
                              setState(() {
                                selectedPeriod = val;
                              });
                            }
                          },
                        ),
                        const SizedBox(height: 16),"""

new_period_widget = """                        // Period Selection Buttons (Morning / Evening)
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                            Text(
                              'الفترة الدراسية للكورس',
                              style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: subTextColor),
                            ),
                            const SizedBox(height: 8),
                            Row(
                              children: [
                                Expanded(
                                  child: InkWell(
                                    onTap: () {
                                      setState(() {
                                        selectedPeriod = 'morning';
                                      });
                                    },
                                    borderRadius: BorderRadius.circular(8),
                                    child: Container(
                                      padding: const EdgeInsets.symmetric(vertical: 14),
                                      decoration: BoxDecoration(
                                        color: selectedPeriod == 'morning' ? AppColors.primary : fieldBg,
                                        borderRadius: BorderRadius.circular(8),
                                        border: Border.all(
                                          color: selectedPeriod == 'morning' ? AppColors.primary : borderColor,
                                        ),
                                      ),
                                      child: Center(
                                        child: Row(
                                          mainAxisAlignment: MainAxisAlignment.center,
                                          children: [
                                            Icon(
                                              Icons.wb_sunny_rounded,
                                              size: 16,
                                              color: selectedPeriod == 'morning' ? Colors.white : AppColors.primary,
                                            ),
                                            const SizedBox(width: 8),
                                            Text(
                                              'صباحي',
                                              style: TextStyle(
                                                color: selectedPeriod == 'morning' ? Colors.white : textColor,
                                                fontWeight: FontWeight.bold,
                                                fontSize: 13,
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                                const SizedBox(width: 16),
                                Expanded(
                                  child: InkWell(
                                    onTap: () {
                                      setState(() {
                                        selectedPeriod = 'evening';
                                      });
                                    },
                                    borderRadius: BorderRadius.circular(8),
                                    child: Container(
                                      padding: const EdgeInsets.symmetric(vertical: 14),
                                      decoration: BoxDecoration(
                                        color: selectedPeriod == 'evening' ? AppColors.primary : fieldBg,
                                        borderRadius: BorderRadius.circular(8),
                                        border: Border.all(
                                          color: selectedPeriod == 'evening' ? AppColors.primary : borderColor,
                                        ),
                                      ),
                                      child: Center(
                                        child: Row(
                                          mainAxisAlignment: MainAxisAlignment.center,
                                          children: [
                                            Icon(
                                              Icons.nights_stay_rounded,
                                              size: 16,
                                              color: selectedPeriod == 'evening' ? Colors.white : AppColors.primary,
                                            ),
                                            const SizedBox(width: 8),
                                            Text(
                                              'مسائي',
                                              style: TextStyle(
                                                color: selectedPeriod == 'evening' ? Colors.white : textColor,
                                                fontWeight: FontWeight.bold,
                                                fontSize: 13,
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),"""

# Apply replacement of period selector in both Add and Edit Dialogs
content = content.replace(old_period_dropdown_add, new_period_widget)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("UI Updates completed successfully!")
