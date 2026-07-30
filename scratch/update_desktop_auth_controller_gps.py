import re

file_path = r"C:\Users\alial\institute_desktop\lib\controllers\auth_controller.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add properties
old_properties = """  final RxString instituteCategory = ''.obs;
  final RxString instituteLatitude = ''.obs;
  final RxString instituteLongitude = ''.obs;"""

new_properties = """  final RxString instituteCategory = ''.obs;
  final RxString instituteLatitude = ''.obs;
  final RxString instituteLongitude = ''.obs;
  final RxString adminRole = 'admin'.obs;
  final RxString adminPermissions = 'all'.obs;"""

content = content.replace(old_properties, new_properties)

# 2. Update _loadSession
old_load = """    instituteCategory.value = prefs.getString('institute_category') ?? '';
    instituteLatitude.value = prefs.getString('institute_latitude') ?? '';
    instituteLongitude.value = prefs.getString('institute_longitude') ?? '';
  }"""

new_load = """    instituteCategory.value = prefs.getString('institute_category') ?? '';
    instituteLatitude.value = prefs.getString('institute_latitude') ?? '';
    instituteLongitude.value = prefs.getString('institute_longitude') ?? '';
    adminRole.value = prefs.getString('admin_role') ?? 'admin';
    adminPermissions.value = prefs.getString('admin_permissions') ?? 'all';
  }"""

content = content.replace(old_load, new_load)

# 3. Update login
old_save = """        instituteCategory.value = data['institute']['category'] ?? '';
        instituteLatitude.value = latVal;
        instituteLongitude.value = lngVal;

        // Reset logo on new login if not cached locally, or keep cached
        instituteLogoUrl.value = prefs.getString('institute_logo_url') ?? '';"""

new_save = """        instituteCategory.value = data['institute']['category'] ?? '';
        instituteLatitude.value = latVal;
        instituteLongitude.value = lngVal;
        
        final rVal = data['admin']['role'] ?? 'admin';
        final pVal = data['admin']['permissions'] ?? 'all';
        await prefs.setString('admin_role', rVal);
        await prefs.setString('admin_permissions', pVal);
        adminRole.value = rVal;
        adminPermissions.value = pVal;

        // Reset logo on new login if not cached locally, or keep cached
        instituteLogoUrl.value = prefs.getString('institute_logo_url') ?? '';"""

content = content.replace(old_save, new_save)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("AuthController in institute app updated to store staff roles & permissions!")
