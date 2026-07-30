import re

file_path = r"C:\Users\alial\student\lib\controllers\auth_controller.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update registerStudent to store temp_email
old_register_save = """      if (response.statusCode == 201 || response.statusCode == 200) {
        final studentData = response.data['student'];
        if (studentData != null) {
          studentId.value = studentData['id'] ?? '';
        }
        isLoading.value = false;
        return true;
      }"""

new_register_save = """      if (response.statusCode == 201 || response.statusCode == 200) {
        final studentData = response.data['student'];
        if (studentData != null) {
          studentId.value = studentData['id'] ?? '';
        }
        // Save email locally for verification fallback
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('temp_email', email.value);
        
        isLoading.value = false;
        return true;
      }"""

content = content.replace(old_register_save, new_register_save)

# 2. Update verifyEmail to restore email if empty
old_verify_start = """  Future<bool> verifyEmail(String code) async {
    isLoading.value = true;
    lastErrorMessage.value = '';

    if (AppConfig.IS_DEMO_MODE) {"""

new_verify_start = """  Future<bool> verifyEmail(String code) async {
    isLoading.value = true;
    lastErrorMessage.value = '';
    
    final prefs = await SharedPreferences.getInstance();
    if (email.value.isEmpty) {
      email.value = prefs.getString('temp_email') ?? '';
    }

    if (AppConfig.IS_DEMO_MODE) {"""

content = content.replace(old_verify_start, new_verify_start)

# 3. Update resendCode to restore email if empty
old_resend_start = """  Future<bool> resendCode() async {
    isLoading.value = true;
    lastErrorMessage.value = '';

    if (AppConfig.IS_DEMO_MODE) {"""

new_resend_start = """  Future<bool> resendCode() async {
    isLoading.value = true;
    lastErrorMessage.value = '';

    final prefs = await SharedPreferences.getInstance();
    if (email.value.isEmpty) {
      email.value = prefs.getString('temp_email') ?? '';
    }
    if (email.value.isEmpty) {
      Get.snackbar('خطأ', 'البريد الإلكتروني غير متوفر، يرجى إعادة تسجيل الحساب!');
      isLoading.value = false;
      return false;
    }

    if (AppConfig.IS_DEMO_MODE) {"""

content = content.replace(old_resend_start, new_resend_start)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("StudentAuthController email persistence fix applied successfully!")
