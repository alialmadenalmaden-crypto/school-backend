import re

file_path = r"C:\Users\alial\institute_desktop\lib\pages\courses\manage_courses_page.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Define the new _showAddCourseDialog implementation
new_add_dialog = """  void _showAddCourseDialog(BuildContext context, CoursesController controller) {
    final titleController = TextEditingController();
    final descriptionController = TextEditingController();
    final instructorController = TextEditingController();
    final priceController = TextEditingController();
    final seatsController = TextEditingController(text: '30');
    final deadlineController = TextEditingController();
    final startController = TextEditingController();
    final endController = TextEditingController();
    final timeController = TextEditingController(text: '10:00 - 12:00');

    final authController = Get.find<AuthController>();
    final rawCats = authController.instituteCategory.value;
    final allowedCategories = rawCats.isNotEmpty
        ? rawCats.split(',').map((c) => c.trim()).where((c) => c.isNotEmpty).toList()
        : <String>[];
    if (allowedCategories.isEmpty) {
      allowedCategories.addAll(['اللغات - إنجليزية', 'الحاسوب']);
    }
    String selectedCategory = allowedCategories.first;

    String? selectedProgramId;
    String? selectedLevelId;
    String? selectedLanguageId;
    String? selectedCurriculumId;

    final isDark = Theme.of(context).brightness == Brightness.dark;
    final textColor = isDark ? Colors.white : AppColors.textPrimary;
    final subTextColor = isDark ? const Color(0xFF94A3B8) : AppColors.textSecondary;
    final cardColor = isDark ? const Color(0xFF1E293B) : Colors.white;
    final borderColor = isDark ? const Color(0xFF334155) : AppColors.border;
    final fieldBg = isDark ? const Color(0xFF0F172A) : AppColors.background;

    showDialog(
      context: context,
      builder: (context) {
        return StatefulBuilder(
          builder: (context, setState) {
            return Directionality(
              textDirection: TextDirection.rtl,
              child: AlertDialog(
                backgroundColor: cardColor,
                surfaceTintColor: Colors.transparent,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                title: Row(
                  children: [
                    const Icon(Icons.add_card_rounded, color: AppColors.primary, size: 28),
                    const SizedBox(width: 8),
                    Text(
                      'إضافة كورس تدريبي جديد',
                      style: TextStyle(fontWeight: FontWeight.bold, color: textColor),
                    ),
                  ],
                ),
                content: Container(
                  width: 550,
                  color: Colors.transparent,
                  child: SingleChildScrollView(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Text(
                          'الرجاء تعبئة كافة تفاصيل الكورس لتسجيله وعرضه للطلاب على المنصة.',
                          style: TextStyle(color: subTextColor, fontSize: 13),
                        ),
                        const SizedBox(height: 20),
                        
                        // Row 1: Title and Instructor
                        Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: titleController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                decoration: InputDecoration(
                                  labelText: 'عنوان الكورس',
                                  labelStyle: TextStyle(color: subTextColor),
                                  hintText: 'مثال: دبلوم بايثون الشامل',
                                  hintStyle: const TextStyle(color: Colors.grey),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.title_rounded),
                                ),
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: TextField(
                                controller: instructorController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                decoration: InputDecoration(
                                  labelText: 'اسم المدرب',
                                  labelStyle: TextStyle(color: subTextColor),
                                  hintText: 'مثال: أ. صالح محمد',
                                  hintStyle: const TextStyle(color: Colors.grey),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.person_rounded),
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        
                        // Row 2: Price and Seats
                        Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: priceController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                keyboardType: TextInputType.number,
                                decoration: InputDecoration(
                                  labelText: 'سعر الكورس (ريال يمني)',
                                  labelStyle: TextStyle(color: subTextColor),
                                  hintText: '0.0',
                                  hintStyle: const TextStyle(color: Colors.grey),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.attach_money_rounded),
                                ),
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: TextField(
                                controller: seatsController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                keyboardType: TextInputType.number,
                                decoration: InputDecoration(
                                  labelText: 'المقاعد المتاحة',
                                  labelStyle: TextStyle(color: subTextColor),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.people_alt_rounded),
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        
                        // Row 3: Registration Deadline & Time
                        Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: deadlineController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                decoration: InputDecoration(
                                  labelText: 'آخر موعد للتسجيل',
                                  labelStyle: TextStyle(color: subTextColor),
                                  hintText: 'YYYY-MM-DD',
                                  hintStyle: const TextStyle(color: Colors.grey),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.event_busy_rounded),
                                ),
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: TextField(
                                controller: timeController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                decoration: InputDecoration(
                                  labelText: 'وقت المحاضرة اليومي',
                                  labelStyle: TextStyle(color: subTextColor),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.watch_later_outlined),
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        
                        // Row 4: Start Date and End Date
                        Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: startController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                decoration: InputDecoration(
                                  labelText: 'تاريخ بدء الدراسة',
                                  labelStyle: TextStyle(color: subTextColor),
                                  hintText: 'YYYY-MM-DD',
                                  hintStyle: const TextStyle(color: Colors.grey),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.date_range_rounded),
                                ),
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: TextField(
                                controller: endController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                decoration: InputDecoration(
                                  labelText: 'تاريخ انتهاء الدراسة',
                                  labelStyle: TextStyle(color: subTextColor),
                                  hintText: 'YYYY-MM-DD',
                                  hintStyle: const TextStyle(color: Colors.grey),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.date_range_rounded),
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        
                        // Category Selection Dropdown
                        DropdownButtonFormField<String>(
                          value: selectedCategory,
                          dropdownColor: cardColor,
                          style: TextStyle(color: textColor, fontSize: 13),
                          decoration: InputDecoration(
                            labelText: 'القسم/التخصص التابع له الكورس',
                            labelStyle: TextStyle(color: subTextColor),
                            filled: true,
                            fillColor: fieldBg,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            prefixIcon: const Icon(Icons.category_rounded, color: AppColors.primary),
                          ),
                          items: allowedCategories.map((cat) {
                            return DropdownMenuItem<String>(
                              value: cat,
                              child: Text(cat, style: TextStyle(color: textColor)),
                            );
                          }).toList(),
                          onChanged: (val) {
                            if (val != null) {
                              selectedCategory = val;
                            }
                          },
                        ),
                        const SizedBox(height: 16),

                        // Program Dropdown
                        DropdownButtonFormField<String>(
                          value: selectedProgramId,
                          dropdownColor: cardColor,
                          style: TextStyle(color: textColor, fontSize: 13),
                          decoration: InputDecoration(
                            labelText: 'البرنامج الدراسي (اختياري)',
                            labelStyle: TextStyle(color: subTextColor),
                            filled: true,
                            fillColor: fieldBg,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            prefixIcon: const Icon(Icons.school_rounded, color: AppColors.primary),
                          ),
                          items: [
                            const DropdownMenuItem<String>(
                              value: null,
                              child: Text('بدون برنامج محدد', style: TextStyle(color: Colors.grey)),
                            ),
                            ...controller.programsList.map((prog) {
                              return DropdownMenuItem<String>(
                                value: prog['id'],
                                child: Text(prog['name'] ?? '', style: TextStyle(color: textColor)),
                              );
                            }).toList(),
                          ],
                          onChanged: (val) {
                            setState(() {
                              selectedProgramId = val;
                            });
                          },
                        ),
                        const SizedBox(height: 16),

                        // Level Dropdown
                        DropdownButtonFormField<String>(
                          value: selectedLevelId,
                          dropdownColor: cardColor,
                          style: TextStyle(color: textColor, fontSize: 13),
                          decoration: InputDecoration(
                            labelText: 'المستوى الدراسي (اختياري)',
                            labelStyle: TextStyle(color: subTextColor),
                            filled: true,
                            fillColor: fieldBg,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            prefixIcon: const Icon(Icons.stacked_bar_chart_rounded, color: AppColors.primary),
                          ),
                          items: [
                            const DropdownMenuItem<String>(
                              value: null,
                              child: Text('بدون مستوى محدد', style: TextStyle(color: Colors.grey)),
                            ),
                            ...controller.levelsList.map((lvl) {
                              return DropdownMenuItem<String>(
                                value: lvl['id'],
                                child: Text(lvl['name'] ?? '', style: TextStyle(color: textColor)),
                              );
                            }).toList(),
                          ],
                          onChanged: (val) {
                            setState(() {
                              selectedLevelId = val;
                            });
                          },
                        ),
                        const SizedBox(height: 16),

                        // Language Dropdown
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
                        ),
                        const SizedBox(height: 16),

                        // Curriculum Dropdown
                        DropdownButtonFormField<String>(
                          value: selectedCurriculumId,
                          dropdownColor: cardColor,
                          style: TextStyle(color: textColor, fontSize: 13),
                          decoration: InputDecoration(
                            labelText: 'المنهج/الكتاب الدراسي (اختياري)',
                            labelStyle: TextStyle(color: subTextColor),
                            filled: true,
                            fillColor: fieldBg,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            prefixIcon: const Icon(Icons.book_rounded, color: AppColors.primary),
                          ),
                          items: [
                            const DropdownMenuItem<String>(
                              value: null,
                              child: Text('بدون منهج محدد', style: TextStyle(color: Colors.grey)),
                            ),
                            ...controller.curriculumsList.map((curr) {
                              return DropdownMenuItem<String>(
                                value: curr['id'],
                                child: Text(curr['name'] ?? '', style: TextStyle(color: textColor)),
                              );
                            }).toList(),
                          ],
                          onChanged: (val) {
                            setState(() {
                              selectedCurriculumId = val;
                            });
                          },
                        ),
                        const SizedBox(height: 16),
                        
                        // Description
                        TextField(
                          controller: descriptionController,
                          style: TextStyle(color: textColor, fontSize: 13),
                          decoration: InputDecoration(
                            labelText: 'وصف تفصيلي ومحاور الكورس',
                            labelStyle: TextStyle(color: subTextColor),
                            hintText: 'اكتب تفاصيل الكورس، متطلباته، والمحاور التي سيتم تغطيتها...',
                            hintStyle: const TextStyle(color: Colors.grey),
                            filled: true,
                            fillColor: fieldBg,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            prefixIcon: const Icon(Icons.description_outlined),
                          ),
                          maxLines: 4,
                        ),
                      ],
                    ),
                  ),
                ),
                actions: [
                  TextButton(
                    onPressed: () => Navigator.pop(context),
                    child: const Text('إلغاء', style: TextStyle(color: Colors.grey, fontWeight: FontWeight.bold)),
                  ),
                  const SizedBox(width: 8),
                  ElevatedButton(
                    onPressed: () async {
                      if (titleController.text.isNotEmpty) {
                        final price = double.tryParse(priceController.text) ?? 0.0;
                        final seats = int.tryParse(seatsController.text) ?? 30;
                        
                        bool success = await controller.addCourse(
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
                        );
                        
                        if (success && context.mounted) {
                          Navigator.pop(context);
                          Get.snackbar(
                            'نجاح الإضافة',
                            'تم تسجيل ونشر الدورة الجديدة بنجاح على المنصة!',
                            snackPosition: SnackPosition.BOTTOM,
                            backgroundColor: AppColors.success,
                            colorText: Colors.white,
                            margin: const EdgeInsets.all(16),
                          );
                        }
                      }
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primary,
                      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                    ),
                    child: const Text('إضافة الكورس', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
            );
          }
        );
      },
    );
  }"""

# Define the new _showEditCourseDialog implementation
new_edit_dialog = """  void _showEditCourseDialog(BuildContext context, CoursesController controller, CourseModel course) {
    final titleController = TextEditingController(text: course.title);
    final descriptionController = TextEditingController(text: course.description);
    final instructorController = TextEditingController(text: course.instructorName);
    final priceController = TextEditingController(text: course.price.toString());
    final seatsController = TextEditingController(text: course.seatsAvailable.toString());
    final deadlineController = TextEditingController(text: course.registrationDeadline);
    final startController = TextEditingController(text: course.startDate);
    final endController = TextEditingController(text: course.endDate);
    final timeController = TextEditingController(text: course.classTime ?? '08:00 - 10:00');

    final authController = Get.find<AuthController>();
    final rawCats = authController.instituteCategory.value;
    final allowedCategories = rawCats.isNotEmpty
        ? rawCats.split(',').map((c) => c.trim()).where((c) => c.isNotEmpty).toList()
        : <String>[];
    if (allowedCategories.isEmpty) {
      allowedCategories.addAll(['اللغات - إنجليزية', 'الحاسوب']);
    }
    String selectedCategory = allowedCategories.contains(course.categoryName)
        ? course.categoryName
        : allowedCategories.first;

    String? selectedProgramId = course.programId;
    String? selectedLevelId = course.levelId;
    String? selectedLanguageId = course.languageId;
    String? selectedCurriculumId = course.curriculumId;

    final isDark = Theme.of(context).brightness == Brightness.dark;
    final textColor = isDark ? Colors.white : AppColors.textPrimary;
    final subTextColor = isDark ? const Color(0xFF94A3B8) : AppColors.textSecondary;
    final cardColor = isDark ? const Color(0xFF1E293B) : Colors.white;
    final borderColor = isDark ? const Color(0xFF334155) : AppColors.border;
    final fieldBg = isDark ? const Color(0xFF0F172A) : AppColors.background;

    showDialog(
      context: context,
      builder: (context) {
        return StatefulBuilder(
          builder: (context, setState) {
            return Directionality(
              textDirection: TextDirection.rtl,
              child: AlertDialog(
                backgroundColor: cardColor,
                surfaceTintColor: Colors.transparent,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                title: Row(
                  children: [
                    const Icon(Icons.edit_note_rounded, color: AppColors.primary, size: 28),
                    const SizedBox(width: 8),
                    Text(
                      'تعديل بيانات الكورس',
                      style: TextStyle(fontWeight: FontWeight.bold, color: textColor),
                    ),
                  ],
                ),
                content: Container(
                  width: 550,
                  color: Colors.transparent,
                  child: SingleChildScrollView(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Text(
                          'تعديل تفاصيل الكورس التدريبي وتحديث بياناته على المنصة للطلاب.',
                          style: TextStyle(color: subTextColor, fontSize: 13),
                        ),
                        const SizedBox(height: 20),
                        
                        // Row 1: Title and Instructor
                        Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: titleController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                decoration: InputDecoration(
                                  labelText: 'عنوان الكورس',
                                  labelStyle: TextStyle(color: subTextColor),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.title_rounded),
                                ),
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: TextField(
                                controller: instructorController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                decoration: InputDecoration(
                                  labelText: 'اسم المدرب',
                                  labelStyle: TextStyle(color: subTextColor),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.person_rounded),
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        
                        // Row 2: Price and Seats
                        Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: priceController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                keyboardType: TextInputType.number,
                                decoration: InputDecoration(
                                  labelText: 'سعر الكورس (ريال يمني)',
                                  labelStyle: TextStyle(color: subTextColor),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.attach_money_rounded),
                                ),
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: TextField(
                                controller: seatsController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                keyboardType: TextInputType.number,
                                decoration: InputDecoration(
                                  labelText: 'المقاعد المتاحة',
                                  labelStyle: TextStyle(color: subTextColor),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.people_alt_rounded),
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        
                        // Row 3: Registration Deadline & Time
                        Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: deadlineController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                decoration: InputDecoration(
                                  labelText: 'آخر موعد للتسجيل',
                                  labelStyle: TextStyle(color: subTextColor),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.event_busy_rounded),
                                ),
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: TextField(
                                controller: timeController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                decoration: InputDecoration(
                                  labelText: 'وقت المحاضرة اليومي',
                                  labelStyle: TextStyle(color: subTextColor),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.watch_later_outlined),
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        
                        // Row 4: Start Date and End Date
                        Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: startController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                decoration: InputDecoration(
                                  labelText: 'تاريخ بدء الدراسة',
                                  labelStyle: TextStyle(color: subTextColor),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.date_range_rounded),
                                ),
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: TextField(
                                controller: endController,
                                style: TextStyle(color: textColor, fontSize: 13),
                                decoration: InputDecoration(
                                  labelText: 'تاريخ انتهاء الدراسة',
                                  labelStyle: TextStyle(color: subTextColor),
                                  filled: true,
                                  fillColor: fieldBg,
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                                  prefixIcon: const Icon(Icons.date_range_rounded),
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        
                        // Category Selection Dropdown
                        DropdownButtonFormField<String>(
                          value: selectedCategory,
                          dropdownColor: cardColor,
                          style: TextStyle(color: textColor, fontSize: 13),
                          decoration: InputDecoration(
                            labelText: 'القسم/التخصص التابع له الكورس',
                            labelStyle: TextStyle(color: subTextColor),
                            filled: true,
                            fillColor: fieldBg,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            prefixIcon: const Icon(Icons.category_rounded, color: AppColors.primary),
                          ),
                          items: allowedCategories.map((cat) {
                            return DropdownMenuItem<String>(
                              value: cat,
                              child: Text(cat, style: TextStyle(color: textColor)),
                            );
                          }).toList(),
                          onChanged: (val) {
                            if (val != null) {
                              selectedCategory = val;
                            }
                          },
                        ),
                        const SizedBox(height: 16),

                        // Program Dropdown
                        DropdownButtonFormField<String>(
                          value: selectedProgramId,
                          dropdownColor: cardColor,
                          style: TextStyle(color: textColor, fontSize: 13),
                          decoration: InputDecoration(
                            labelText: 'البرنامج الدراسي (اختياري)',
                            labelStyle: TextStyle(color: subTextColor),
                            filled: true,
                            fillColor: fieldBg,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            prefixIcon: const Icon(Icons.school_rounded, color: AppColors.primary),
                          ),
                          items: [
                            const DropdownMenuItem<String>(
                              value: null,
                              child: Text('بدون برنامج محدد', style: TextStyle(color: Colors.grey)),
                            ),
                            ...controller.programsList.map((prog) {
                              return DropdownMenuItem<String>(
                                value: prog['id'],
                                child: Text(prog['name'] ?? '', style: TextStyle(color: textColor)),
                              );
                            }).toList(),
                          ],
                          onChanged: (val) {
                            setState(() {
                              selectedProgramId = val;
                            });
                          },
                        ),
                        const SizedBox(height: 16),

                        // Level Dropdown
                        DropdownButtonFormField<String>(
                          value: selectedLevelId,
                          dropdownColor: cardColor,
                          style: TextStyle(color: textColor, fontSize: 13),
                          decoration: InputDecoration(
                            labelText: 'المستوى الدراسي (اختياري)',
                            labelStyle: TextStyle(color: subTextColor),
                            filled: true,
                            fillColor: fieldBg,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            prefixIcon: const Icon(Icons.stacked_bar_chart_rounded, color: AppColors.primary),
                          ),
                          items: [
                            const DropdownMenuItem<String>(
                              value: null,
                              child: Text('بدون مستوى محدد', style: TextStyle(color: Colors.grey)),
                            ),
                            ...controller.levelsList.map((lvl) {
                              return DropdownMenuItem<String>(
                                value: lvl['id'],
                                child: Text(lvl['name'] ?? '', style: TextStyle(color: textColor)),
                              );
                            }).toList(),
                          ],
                          onChanged: (val) {
                            setState(() {
                              selectedLevelId = val;
                            });
                          },
                        ),
                        const SizedBox(height: 16),

                        // Language Dropdown
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
                        ),
                        const SizedBox(height: 16),

                        // Curriculum Dropdown
                        DropdownButtonFormField<String>(
                          value: selectedCurriculumId,
                          dropdownColor: cardColor,
                          style: TextStyle(color: textColor, fontSize: 13),
                          decoration: InputDecoration(
                            labelText: 'المنهج/الكتاب الدراسي (اختياري)',
                            labelStyle: TextStyle(color: subTextColor),
                            filled: true,
                            fillColor: fieldBg,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            prefixIcon: const Icon(Icons.book_rounded, color: AppColors.primary),
                          ),
                          items: [
                            const DropdownMenuItem<String>(
                              value: null,
                              child: Text('بدون منهج محدد', style: TextStyle(color: Colors.grey)),
                            ),
                            ...controller.curriculumsList.map((curr) {
                              return DropdownMenuItem<String>(
                                value: curr['id'],
                                child: Text(curr['name'] ?? '', style: TextStyle(color: textColor)),
                              );
                            }).toList(),
                          ],
                          onChanged: (val) {
                            setState(() {
                              selectedCurriculumId = val;
                            });
                          },
                        ),
                        const SizedBox(height: 16),
                        
                        // Description
                        TextField(
                          controller: descriptionController,
                          style: TextStyle(color: textColor, fontSize: 13),
                          decoration: InputDecoration(
                            labelText: 'وصف تفصيلي ومحاور الكورس',
                            labelStyle: TextStyle(color: subTextColor),
                            filled: true,
                            fillColor: fieldBg,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide(color: borderColor)),
                            prefixIcon: const Icon(Icons.description_outlined),
                          ),
                          maxLines: 4,
                        ),
                      ],
                    ),
                  ),
                ),
                actions: [
                  TextButton(
                    onPressed: () => Navigator.pop(context),
                    child: const Text('إلغاء', style: TextStyle(color: Colors.grey, fontWeight: FontWeight.bold)),
                  ),
                  const SizedBox(width: 8),
                  ElevatedButton(
                    onPressed: () async {
                      if (titleController.text.isNotEmpty) {
                        final price = double.tryParse(priceController.text) ?? 0.0;
                        final seats = int.tryParse(seatsController.text) ?? 30;
                        
                        bool success = await controller.updateCourse(
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
                        );
                        
                        if (success && context.mounted) {
                          Navigator.pop(context);
                          Get.snackbar(
                            'نجاح التحديث',
                            'تم تحديث تفاصيل الدورة التدريبية بنجاح!',
                            snackPosition: SnackPosition.BOTTOM,
                            backgroundColor: AppColors.success,
                            colorText: Colors.white,
                            margin: const EdgeInsets.all(16),
                          );
                        }
                      }
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primary,
                      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                    ),
                    child: const Text('حفظ التعديلات', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
            );
          }
        );
      },
    );
  }"""

# Find _showAddCourseDialog block and replace it
# Match from `void _showAddCourseDialog` to the matching end of it
pattern_add = r"void _showAddCourseDialog\(BuildContext context, CoursesController controller\) \{.*?\n  \}"
content_updated = re.sub(pattern_add, new_add_dialog, content, flags=re.DOTALL)

# Find _showEditCourseDialog block and replace it
pattern_edit = r"void _showEditCourseDialog\(BuildContext context, CoursesController controller, CourseModel course\) \{.*?\n  \}"
content_updated = re.sub(pattern_edit, new_edit_dialog, content_updated, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content_updated)

print("Replacement successful!")
