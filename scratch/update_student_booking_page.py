import re

file_path = r"C:\Users\alial\student\lib\pages\home\booking_page.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Initialize _notesController and _termsAccepted in _BookingPageState
old_controllers = """  // Controllers
  final TextEditingController _seatsController = TextEditingController(
    text: '1',
  );
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _phoneController = TextEditingController();"""

new_controllers = """  // Controllers
  final TextEditingController _seatsController = TextEditingController(
    text: '1',
  );
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _phoneController = TextEditingController();
  final TextEditingController _notesController = TextEditingController();
  bool _termsAccepted = false;"""

content = content.replace(old_controllers, new_controllers)

# 2. Update _buildTextField to support maxLines parameter
old_build_text_field = """  Widget _buildTextField({
    required TextEditingController controller,
    required String label,
    required IconData icon,
    required bool isDark,
    TextInputType keyboardType = TextInputType.text,
    String? hint,
  }) {
    return Padding(
      padding: EdgeInsets.only(bottom: 15.h),
      child: TextFormField(
        controller: controller,
        keyboardType: keyboardType,
        style: TextStyle(color: Theme.of(context).textTheme.bodyLarge?.color),
        decoration: InputDecoration(
          labelText: label,
          hintText: hint,
          prefixIcon: Padding(
            padding: EdgeInsets.all(8.w),
            child: Container(
              padding: EdgeInsets.all(4.w),
              decoration: const BoxDecoration(
                color: AppColors.primary,
                shape: BoxShape.circle,
              ),
              child: Icon(icon, color: Colors.white, size: 18.sp),
            ),
          ),
        ),
      ),
    );
  }"""

new_build_text_field = """  Widget _buildTextField({
    required TextEditingController controller,
    required String label,
    required IconData icon,
    required bool isDark,
    TextInputType keyboardType = TextInputType.text,
    String? hint,
    int maxLines = 1,
  }) {
    return Padding(
      padding: EdgeInsets.only(bottom: 15.h),
      child: TextFormField(
        controller: controller,
        keyboardType: keyboardType,
        maxLines: maxLines,
        style: TextStyle(color: Theme.of(context).textTheme.bodyLarge?.color),
        decoration: InputDecoration(
          labelText: label,
          hintText: hint,
          prefixIcon: Padding(
            padding: EdgeInsets.all(8.w),
            child: Container(
              padding: EdgeInsets.all(4.w),
              decoration: const BoxDecoration(
                color: AppColors.primary,
                shape: BoxShape.circle,
              ),
              child: Icon(icon, color: Colors.white, size: 18.sp),
            ),
          ),
        ),
      ),
    );
  }"""

content = content.replace(old_build_text_field, new_build_text_field)

# 3. Add notes field, terms box and checkbox in the form
old_form_fields = """                _buildTextField(
                  controller: _phoneController,
                  label: isArabic ? 'رقم الهاتف' : 'Phone Number',
                  icon: Icons.phone_android_rounded,
                  isDark: isDark,
                  keyboardType: TextInputType.phone,
                ),
              ],

              SizedBox(height: 40.h),
              _buildConfirmButton(isArabic, isDark),"""

new_form_fields = """                _buildTextField(
                  controller: _phoneController,
                  label: isArabic ? 'رقم الهاتف' : 'Phone Number',
                  icon: Icons.phone_android_rounded,
                  isDark: isDark,
                  keyboardType: TextInputType.phone,
                ),
                _buildTextField(
                  controller: _notesController,
                  label: isArabic ? 'ملاحظات إضافية للمعهد (اختياري)' : 'Additional Notes (Optional)',
                  icon: Icons.note_alt_outlined,
                  isDark: isDark,
                  maxLines: 3,
                ),
                SizedBox(height: 15.h),

                // Terms and Conditions Box
                Container(
                  padding: EdgeInsets.all(15.w),
                  decoration: BoxDecoration(
                    color: isDark ? const Color(0xFF1E293B) : Colors.orange.shade50,
                    borderRadius: BorderRadius.circular(12.r),
                    border: Border.all(
                      color: isDark ? const Color(0xFF334155) : Colors.orange.shade200,
                      width: 1,
                    ),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.gavel_rounded, color: Colors.orange),
                          SizedBox(width: 8.w),
                          Text(
                            isArabic ? 'شروط وأحكام التسجيل بالمعهد' : 'Institute Registration Terms',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 13.sp,
                              color: isDark ? Colors.white : AppColors.textPrimary,
                            ),
                          ),
                        ],
                      ),
                      SizedBox(height: 10.h),
                      Text(
                        isArabic
                            ? '1. يرجى سداد رسوم الحجز لتأكيد مقعدك في الدورة التدريبية.\\n2. يجب إرفاق صورة إشعار الحوالة (سند القبض) بدقة لإتمام التحقق والموافقة الفورية.\\n3. الحضور والالتزام بالخطة الدراسية للفترة المحددة (صباحي/مسائي) شرط أساسي لحضور الاختبار النهائي.'
                            : '1. Please pay registration fees to confirm your seat.\\n2. The transfer receipt image must be attached accurately for verification.\\n3. Attendance and commitment to the period (morning/evening) is required.',
                        style: TextStyle(
                          fontSize: 11.sp,
                          color: isDark ? Colors.white70 : Colors.black87,
                          height: 1.5,
                        ),
                      ),
                    ],
                  ),
                ),
                SizedBox(height: 12.h),

                // Terms Agreement Checkbox
                Row(
                  children: [
                    Checkbox(
                      value: _termsAccepted,
                      activeColor: AppColors.primary,
                      onChanged: (val) {
                        setState(() {
                          _termsAccepted = val ?? false;
                        });
                      },
                    ),
                    Expanded(
                      child: Text(
                        isArabic ? 'أوافق على كافة الشروط والأحكام المذكورة أعلاه' : 'I agree to the terms and conditions',
                        style: TextStyle(
                          fontSize: 12.sp,
                          fontWeight: FontWeight.bold,
                          color: isDark ? Colors.white70 : AppColors.textPrimary,
                        ),
                      ),
                    ),
                  ],
                ),
              ],

              SizedBox(height: 30.h),
              _buildConfirmButton(isArabic, isDark),"""

content = content.replace(old_form_fields, new_form_fields)

# 4. Update _buildConfirmButton to validate checkbox
old_confirm_press = """  Widget _buildConfirmButton(bool isArabic, bool isDark) {
    return ElevatedButton(
      onPressed: () {
        _showPaymentMethodDialog(isArabic, isDark);
      },"""

new_confirm_press = """  Widget _buildConfirmButton(bool isArabic, bool isDark) {
    return ElevatedButton(
      onPressed: () {
        if (!_termsAccepted) {
          Get.snackbar(
            isArabic ? 'تحذير' : 'Warning',
            isArabic ? 'يرجى الموافقة على شروط المعهد أولاً لإتمام الحجز!' : 'Please agree to the terms first!',
            backgroundColor: Colors.redAccent,
            colorText: Colors.white,
          );
          return;
        }
        _showPaymentMethodDialog(isArabic, isDark);
      },"""

content = content.replace(old_confirm_press, new_confirm_press)

# 5. Pass notes inside request data map
old_add_req_call = """                      Get.find<RequestsController>().addRequest({
                        'course_id': widget.courseData['id'],
                        'title': widget.courseData['title'],
                        'institute': widget.courseData['institute'] ?? widget.courseData['instructor'],
                        'price': widget.courseData['price'],
                        'name': _nameController.text.isNotEmpty ? _nameController.text : (isArabic ? 'غير محدد' : 'Not specified'),
                        'phone': _phoneController.text.isNotEmpty ? _phoneController.text : (isArabic ? 'غير محدد' : 'Not specified'),
                        'payment_method': selectedMethod,
                        'registration_type': isFamilyRegistration ? 'family' : 'personal',
                        'seats': isFamilyRegistration ? _seatsController.text : '1',
                        'receipt_image_path': _selectedImagePath,
                      });"""

new_add_req_call = """                      Get.find<RequestsController>().addRequest({
                        'course_id': widget.courseData['id'],
                        'title': widget.courseData['title'],
                        'institute': widget.courseData['institute'] ?? widget.courseData['instructor'],
                        'price': widget.courseData['price'],
                        'name': _nameController.text.isNotEmpty ? _nameController.text : (isArabic ? 'غير محدد' : 'Not specified'),
                        'phone': _phoneController.text.isNotEmpty ? _phoneController.text : (isArabic ? 'غير محدد' : 'Not specified'),
                        'payment_method': selectedMethod,
                        'registration_type': isFamilyRegistration ? 'family' : 'personal',
                        'seats': isFamilyRegistration ? _seatsController.text : '1',
                        'receipt_image_path': _selectedImagePath,
                        'notes': _notesController.text.trim(),
                      });"""

content = content.replace(old_add_req_call, new_add_req_call)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Student app booking page updated successfully with terms, notes, and verification checkbox!")
