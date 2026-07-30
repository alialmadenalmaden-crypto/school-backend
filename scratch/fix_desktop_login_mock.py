import re

file_path = r"C:\Users\alial\institute_desktop\lib\controllers\auth_controller.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Locate and remove the fallback at the bottom of the catch block
old_fallback = """      if (phone == '777111222' && password == '1234') {
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('token', 'mock_desktop_token');
        await prefs.setString('admin_name', 'مدير معهد يالي (أوفلاين)');
        await prefs.setString('admin_email', 'yali_admin@yali.com');
        await prefs.setString('institute_slug', 'yali');
        await prefs.setString('institute_name', 'معهد يالي (أوفلاين)');
        await prefs.setString('institute_jeep_number', '123456789');
        await prefs.setString(
          'institute_category',
          'اللغات - إنجليزية, الحاسوب',
        );

        instituteId.value = 'mock_institute_id_yali';
        adminName.value = 'مدير معهد يالي (أوفلاين)';
        adminEmail.value = 'yali_admin@yali.com';
        instituteSlug.value = 'yali';
        instituteName.value = 'معهد يالي (أوفلاين)';
        instituteJeepNumber.value = '123456789';
        instituteCategory.value = 'اللغات - إنجليزية, الحاسوب';
        instituteLogoUrl.value = '';

        Get.offAllNamed(AppRoutes.home);
        isLoading.value = false;
        return true;
      }"""

# Remove it (replace with empty string)
content = content.replace(old_fallback, "")

# 2. Add the mock check at the very beginning of the login function
old_login_start = """  Future<bool> login(String phone, String password) async {
    isLoading.value = true;
    errorMessage.value = '';

    try {"""

new_login_start = """  Future<bool> login(String phone, String password) async {
    isLoading.value = true;
    errorMessage.value = '';

    if (phone == '777111222' && password == '1234') {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', 'mock_desktop_token');
      await prefs.setString('admin_name', 'مدير معهد يالي (تجريبي/أوفلاين)');
      await prefs.setString('admin_email', 'yali_admin@yali.com');
      await prefs.setString('institute_slug', 'yali');
      await prefs.setString('institute_name', 'معهد يالي (تجريبي/أوفلاين)');
      await prefs.setString('institute_jeep_number', '123456789');
      await prefs.setString('institute_category', 'اللغات - إنجليزية, الحاسوب');
      await prefs.setString('admin_role', 'admin');
      await prefs.setString('admin_permissions', 'all');

      instituteId.value = 'mock_institute_id_yali';
      adminName.value = 'مدير معهد يالي (تجريبي/أوفلاين)';
      adminEmail.value = 'yali_admin@yali.com';
      instituteSlug.value = 'yali';
      instituteName.value = 'معهد يالي (تجريبي/أوفلاين)';
      instituteJeepNumber.value = '123456789';
      instituteCategory.value = 'اللغات - إنجليزية, الحاسوب';
      instituteLogoUrl.value = '';
      adminRole.value = 'admin';
      adminPermissions.value = 'all';

      Get.offAllNamed(AppRoutes.home);
      isLoading.value = false;
      return true;
    }

    try {"""

content = content.replace(old_login_start, new_login_start)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("AuthController login mock bypass fixed successfully!")
