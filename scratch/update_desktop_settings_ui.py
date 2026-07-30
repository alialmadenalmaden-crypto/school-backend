import re

file_path = r"C:\Users\alial\institute_desktop\lib\pages\settings\settings_page.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add geolocator import
content = "import 'package:geolocator/geolocator.dart';\n" + content

# 2. Add controllers definition
old_controllers = """  final TextEditingController _confirmPasswordController = TextEditingController();
  final TextEditingController _jeepNumberController = TextEditingController();"""

new_controllers = """  final TextEditingController _confirmPasswordController = TextEditingController();
  final TextEditingController _jeepNumberController = TextEditingController();
  final TextEditingController _latitudeController = TextEditingController();
  final TextEditingController _longitudeController = TextEditingController();"""

content = content.replace(old_controllers, new_controllers)

# 3. Add initState initialization
old_init_state = """  @override
  void initState() {
    super.initState();
    _jeepNumberController.text = _authController.instituteJeepNumber.value;
  }"""

new_init_state = """  @override
  void initState() {
    super.initState();
    _jeepNumberController.text = _authController.instituteJeepNumber.value;
    _latitudeController.text = _authController.instituteLatitude.value;
    _longitudeController.text = _authController.instituteLongitude.value;
  }"""

content = content.replace(old_init_state, new_init_state)

# 4. Add dispose cleanup
old_dispose = """    _confirmPasswordController.dispose();
    _jeepNumberController.dispose();
    super.dispose();"""

new_dispose = """    _confirmPasswordController.dispose();
    _jeepNumberController.dispose();
    _latitudeController.dispose();
    _longitudeController.dispose();
    super.dispose();"""

content = content.replace(old_dispose, new_dispose)

# 5. Add geolocator location helper method inside _SettingsPageState
old_submit_password = """  Future<void> _submitChangePassword() async {"""

new_helper_methods = """  Future<void> _getCurrentLocation() async {
    try {
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        Get.snackbar('تنبيه', 'الرجاء تفعيل خدمة تحديد الموقع (GPS) في جهازك!',
            backgroundColor: AppColors.error, colorText: Colors.white);
        return;
      }

      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          Get.snackbar('تنبيه', 'تم رفض إذن الوصول للموقع الجغرافي!',
              backgroundColor: AppColors.error, colorText: Colors.white);
          return;
        }
      }

      if (permission == LocationPermission.deniedForever) {
        Get.snackbar('تنبيه', 'إذن الوصول للموقع مرفوض بشكل دائم. الرجاء تفعيله من إعدادات النظام.',
            backgroundColor: AppColors.error, colorText: Colors.white);
        return;
      }

      Position position = await Geolocator.getCurrentPosition(
          desiredAccuracy: LocationAccuracy.high);
      
      setState(() {
        _latitudeController.text = position.latitude.toString();
        _longitudeController.text = position.longitude.toString();
      });
      
      Get.snackbar('نجاح', 'تم تحديد إحداثيات موقعك الحالي بنجاح!',
          backgroundColor: AppColors.success, colorText: Colors.white);
    } catch (e) {
      Get.snackbar('خطأ', 'فشل تحديد الموقع: $e',
          backgroundColor: AppColors.error, colorText: Colors.white);
    }
  }

  Future<void> _submitChangePassword() async {"""

content = content.replace(old_submit_password, new_helper_methods)

# 6. Update _submitChangeJeepNumber to call updateSettings with coords
old_submit_jeep = """  Future<void> _submitChangeJeepNumber() async {
    if (!_jeepFormKey.currentState!.validate()) return;

    final success = await _authController.updateJeepNumber(
      _jeepNumberController.text,
    );"""

new_submit_jeep = """  Future<void> _submitChangeJeepNumber() async {
    if (!_jeepFormKey.currentState!.validate()) return;

    final success = await _authController.updateSettings(
      jeepNumber: _jeepNumberController.text,
      latitude: double.tryParse(_latitudeController.text),
      longitude: double.tryParse(_longitudeController.text),
    );"""

content = content.replace(old_submit_jeep, new_submit_jeep)

# 7. Add Coordinates UI Fields & Get GPS Location Button under Jeep field
old_jeep_textformfield = """                                TextFormField(
                                  controller: _jeepNumberController,
                                  keyboardType: TextInputType.number,
                                  style: TextStyle(color: textColor, fontSize: 13),
                                  decoration: InputDecoration(
                                    hintText: 'أدخل رقم المحفظة (مثال: 123456789)',
                                    hintStyle: const TextStyle(fontSize: 13, color: Colors.grey),
                                    prefixIcon: const Icon(Icons.pin_rounded, color: Colors.grey),
                                    filled: true,
                                    fillColor: fieldBgColor,
                                    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                                    border: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(10),
                                      borderSide: BorderSide(color: borderColor),
                                    ),
                                    enabledBorder: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(10),
                                      borderSide: BorderSide(color: borderColor),
                                    ),
                                    focusedBorder: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(10),
                                      borderSide: const BorderSide(color: AppColors.primary, width: 1.5),
                                    ),
                                  ),
                                  validator: (val) {
                                    if (val == null || val.isEmpty) {
                                      return 'يرجى إدخال رقم محفظة جيب الخاص بالمعهد!';
                                    }
                                    return null;
                                  },
                                ),
                                const SizedBox(height: 32),"""

new_gps_fields_ui = """                                TextFormField(
                                  controller: _jeepNumberController,
                                  keyboardType: TextInputType.number,
                                  style: TextStyle(color: textColor, fontSize: 13),
                                  decoration: InputDecoration(
                                    hintText: 'أدخل رقم المحفظة (مثال: 123456789)',
                                    hintStyle: const TextStyle(fontSize: 13, color: Colors.grey),
                                    prefixIcon: const Icon(Icons.pin_rounded, color: Colors.grey),
                                    filled: true,
                                    fillColor: fieldBgColor,
                                    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                                    border: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(10),
                                      borderSide: BorderSide(color: borderColor),
                                    ),
                                    enabledBorder: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(10),
                                      borderSide: BorderSide(color: borderColor),
                                    ),
                                    focusedBorder: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(10),
                                      borderSide: const BorderSide(color: AppColors.primary, width: 1.5),
                                    ),
                                  ),
                                  validator: (val) {
                                    if (val == null || val.isEmpty) {
                                      return 'يرجى إدخال رقم محفظة جيب الخاص بالمعهد!';
                                    }
                                    return null;
                                  },
                                ),
                                const SizedBox(height: 24),

                                // GPS Coordinates Header and Action
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      'الموقع الجغرافي للمعهد (إحداثيات GPS)',
                                      style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        color: textColor,
                                        fontSize: 13,
                                      ),
                                    ),
                                    TextButton.icon(
                                      onPressed: _getCurrentLocation,
                                      icon: const Icon(Icons.my_location_rounded, size: 16, color: AppColors.primary),
                                      label: const Text(
                                        'تحديد موقعي الحالي',
                                        style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 12),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 8),

                                // Row containing Lat / Lng inputs
                                Row(
                                  children: [
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            'خط العرض (Latitude)',
                                            style: TextStyle(fontSize: 11, color: subTextColor),
                                          ),
                                          const SizedBox(height: 4),
                                          TextFormField(
                                            controller: _latitudeController,
                                            keyboardType: const TextInputType.numberWithOptions(decimal: true),
                                            style: TextStyle(color: textColor, fontSize: 13),
                                            decoration: InputDecoration(
                                              hintText: 'مثال: 15.35623',
                                              hintStyle: const TextStyle(fontSize: 13, color: Colors.grey),
                                              prefixIcon: const Icon(Icons.location_on_rounded, color: Colors.grey),
                                              filled: true,
                                              fillColor: fieldBgColor,
                                              contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
                                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide(color: borderColor)),
                                              enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide(color: borderColor)),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                    const SizedBox(width: 16),
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            'خط الطول (Longitude)',
                                            style: TextStyle(fontSize: 11, color: subTextColor),
                                          ),
                                          const SizedBox(height: 4),
                                          TextFormField(
                                            controller: _longitudeController,
                                            keyboardType: const TextInputType.numberWithOptions(decimal: true),
                                            style: TextStyle(color: textColor, fontSize: 13),
                                            decoration: InputDecoration(
                                              hintText: 'مثال: 44.19532',
                                              hintStyle: const TextStyle(fontSize: 13, color: Colors.grey),
                                              prefixIcon: const Icon(Icons.location_on_rounded, color: Colors.grey),
                                              filled: true,
                                              fillColor: fieldBgColor,
                                              contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
                                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide(color: borderColor)),
                                              enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide(color: borderColor)),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 32),"""

content = content.replace(old_jeep_textformfield, new_gps_fields_ui)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Desktop settings UI updated with GPS controls successfully!")
