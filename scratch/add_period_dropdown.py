import re

file_path = r"C:\Users\alial\institute_desktop\lib\pages\courses\manage_courses_page.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Define the period dropdown code block for Add Course Dialog
add_period_vars = """    String? selectedProgramId;
    String? selectedLevelId;
    String? selectedLanguageId;
    String? selectedCurriculumId;
    String selectedPeriod = 'morning';"""

# Replace the variables list in add dialog
content = content.replace(
    """    String? selectedProgramId;
    String? selectedLevelId;
    String? selectedLanguageId;
    String? selectedCurriculumId;""",
    add_period_vars
)

# Insert the period dropdown widget below the category dropdown in Add Dialog
# Category dropdown in Add Dialog is followed by `const SizedBox(height: 16),` and then `// Program Dropdown`
old_dropdown_section_add = """                        // Program Dropdown
                        DropdownButtonFormField<String>("""

new_dropdown_section_add = """                        // Period Selection Dropdown (Morning / Evening)
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
                        const SizedBox(height: 16),

                        // Program Dropdown
                        DropdownButtonFormField<String>("""

content = content.replace(old_dropdown_section_add, new_dropdown_section_add)

# Pass selectedPeriod in addCourse call
old_add_call = """                        bool success = await controller.addCourse(
                          title: titleController.text.trim(),
                          description: descriptionController.text.trim(),
                          instructor: instructorController.text.trim(),
                          price: price,
                          seatsAvailable: seats,
                          registrationDeadline: deadlineController.text,
                          startDate: startController.text,
                          endDate: endController.text,
                          classTime: timeController.text.trim(),
                          categoryName: selectedCategory,
                          programId: selectedProgramId,
                          levelId: selectedLevelId,
                          languageId: selectedLanguageId,
                          curriculumId: selectedCurriculumId,
                        );"""

new_add_call = """                        bool success = await controller.addCourse(
                          title: titleController.text.trim(),
                          description: descriptionController.text.trim(),
                          instructor: instructorController.text.trim(),
                          price: price,
                          seatsAvailable: seats,
                          registrationDeadline: deadlineController.text,
                          startDate: startController.text,
                          endDate: endController.text,
                          classTime: timeController.text.trim(),
                          categoryName: selectedCategory,
                          programId: selectedProgramId,
                          levelId: selectedLevelId,
                          languageId: selectedLanguageId,
                          curriculumId: selectedCurriculumId,
                          period: selectedPeriod,
                        );"""

content = content.replace(old_add_call, new_add_call)

# Now, same for Edit Dialog:
edit_period_vars = """    String? selectedProgramId = course.programId;
    String? selectedLevelId = course.levelId;
    String? selectedLanguageId = course.languageId;
    String? selectedCurriculumId = course.curriculumId;
    String selectedPeriod = course.period ?? 'morning';"""

content = content.replace(
    """    String? selectedProgramId = course.programId;
    String? selectedLevelId = course.levelId;
    String? selectedLanguageId = course.languageId;
    String? selectedCurriculumId = course.curriculumId;""",
    edit_period_vars
)

# Replace the editCourse call to pass selectedPeriod
old_edit_call = """                        bool success = await controller.updateCourse(
                          course.id,
                          title: titleController.text.trim(),
                          description: descriptionController.text.trim(),
                          instructor: instructorController.text.trim(),
                          price: price,
                          seatsAvailable: seats,
                          registrationDeadline: deadlineController.text,
                          startDate: startController.text,
                          endDate: endController.text,
                          classTime: timeController.text.trim(),
                          categoryName: selectedCategory,
                          programId: selectedProgramId,
                          levelId: selectedLevelId,
                          languageId: selectedLanguageId,
                          curriculumId: selectedCurriculumId,
                        );"""

new_edit_call = """                        bool success = await controller.updateCourse(
                          course.id,
                          title: titleController.text.trim(),
                          description: descriptionController.text.trim(),
                          instructor: instructorController.text.trim(),
                          price: price,
                          seatsAvailable: seats,
                          registrationDeadline: deadlineController.text,
                          startDate: startController.text,
                          endDate: endController.text,
                          classTime: timeController.text.trim(),
                          categoryName: selectedCategory,
                          programId: selectedProgramId,
                          levelId: selectedLevelId,
                          languageId: selectedLanguageId,
                          curriculumId: selectedCurriculumId,
                          period: selectedPeriod,
                        );"""

content = content.replace(old_edit_call, new_edit_call)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Period dropdown successfully added to UI!")
