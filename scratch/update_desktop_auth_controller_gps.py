import re

file_path = r"C:\Users\alial\institute_desktop\lib\controllers\auth_controller.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add Rx variables
old_vars = """  final RxString instituteLogoUrl = ''.obs;
  final RxString instituteCategory = ''.obs;"""

new_vars = """  final RxString instituteLogoUrl = ''.obs;
  final RxString instituteCategory = ''.obs;
  final RxString instituteLatitude = ''.obs;
  final RxString instituteLongitude = ''.obs;"""

content = content.replace(old_vars, new_vars)

# Update _loadSession
old_load = """    instituteLogoUrl.value = prefs.getString('institute_logo_url') ?? '';
    instituteCategory.value = prefs.getString('institute_category') ?? '';
  }"""

new_load = """    instituteLogoUrl.value = prefs.getString('institute_logo_url') ?? '';
    instituteCategory.value = prefs.getString('institute_category') ?? '';
    instituteLatitude.value = prefs.getString('institute_latitude') ?? '';
    instituteLongitude.value = prefs.getString('institute_longitude') ?? '';
  }"""

content = content.replace(old_load, new_load)

# Update login response parsing
old_login_parse = """        await prefs.setString(
          'institute_category',
          data['institute']['category'] ?? '',
        );

        instituteId.value = data['institute']['id'] ?? '';
        adminName.value = data['admin']['name'] ?? '';
        adminEmail.value = data['admin']['email'] ?? '';
        instituteSlug.value = data['institute']['slug'] ?? '';
        instituteName.value = data['institute']['name'] ?? '';
        instituteJeepNumber.value = data['institute']['jeep_number'] ?? '';
        instituteCategory.value = data['institute']['category'] ?? '';"""

new_login_parse = """        await prefs.setString(
          'institute_category',
          data['institute']['category'] ?? '',
        );
        final latVal = (data['institute']['latitude'] ?? '').toString();
        final lngVal = (data['institute']['longitude'] ?? '').toString();
        await prefs.setString('institute_latitude', latVal);
        await prefs.setString('institute_longitude', lngVal);

        instituteId.value = data['institute']['id'] ?? '';
        adminName.value = data['admin']['name'] ?? '';
        adminEmail.value = data['admin']['email'] ?? '';
        instituteSlug.value = data['institute']['slug'] ?? '';
        instituteName.value = data['institute']['name'] ?? '';
        instituteJeepNumber.value = data['institute']['jeep_number'] ?? '';
        instituteCategory.value = data['institute']['category'] ?? '';
        instituteLatitude.value = latVal;
        instituteLongitude.value = lngVal;"""

content = content.replace(old_login_parse, new_login_parse)

# Update updateJeepNumber method to updateSettings
old_update_jeep = """  Future<bool> updateJeepNumber(String jeepNumber) async {
    isLoading.value = true;
    errorMessage.value = '';

    try {
      final dio = DioFactory.getDio();
      final response = await dio.post(
        'institutes/admin/update-settings/',
        data: {'email': adminEmail.value, 'jeep_number': jeepNumber},
      );

      if (response.statusCode == 200) {
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('institute_jeep_number', jeepNumber);
        instituteJeepNumber.value = jeepNumber;
        isLoading.value = false;
        return true;
      }
    } catch (e) {
      debugPrint('DIO_UPDATE_SETTINGS_ERROR: $e');
      if (e is DioException && e.response != null) {
        final detail = e.response?.data?['detail'] ?? 'فشل تحديث رقم جيب!';
        errorMessage.value = detail.toString();
      } else {
        errorMessage.value = 'تعذر الاتصال بالسيرفر، يرجى المحاولة لاحقاً!';
      }
    } finally {
      isLoading.value = false;
    }
    return false;
  }"""

new_update_settings = """  Future<bool> updateSettings({
    required String jeepNumber,
    double? latitude,
    double? longitude,
  }) async {
    isLoading.value = true;
    errorMessage.value = '';

    try {
      final dio = DioFactory.getDio();
      final data = {
        'email': adminEmail.value, 
        'jeep_number': jeepNumber,
        if (latitude != null) 'latitude': latitude,
        if (longitude != null) 'longitude': longitude,
      };
      
      final response = await dio.post(
        'institutes/admin/update-settings/',
        data: data,
      );

      if (response.statusCode == 200) {
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('institute_jeep_number', jeepNumber);
        instituteJeepNumber.value = jeepNumber;
        
        final latVal = (response.data['latitude'] ?? '').toString();
        final lngVal = (response.data['longitude'] ?? '').toString();
        await prefs.setString('institute_latitude', latVal);
        await prefs.setString('institute_longitude', lngVal);
        instituteLatitude.value = latVal;
        instituteLongitude.value = lngVal;

        isLoading.value = false;
        return true;
      }
    } catch (e) {
      debugPrint('DIO_UPDATE_SETTINGS_ERROR: $e');
      if (e is DioException && e.response != null) {
        final detail = e.response?.data?['detail'] ?? 'فشل تحديث الإعدادات!';
        errorMessage.value = detail.toString();
      } else {
        errorMessage.value = 'تعذر الاتصال بالسيرفر، يرجى المحاولة لاحقاً!';
      }
    } finally {
      isLoading.value = false;
    }
    return false;
  }"""

content = content.replace(old_update_jeep, new_update_settings)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("AuthController updated in institute_desktop!")
