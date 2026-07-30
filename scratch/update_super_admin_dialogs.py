import re

file_path = r"C:\Users\alial\super_admin_desktop\lib\pages\dashboard\dialogs\institute_dialogs.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add map imports at the top
content = "import 'package:flutter_map/flutter_map.dart';\nimport 'package:latlong2/latlong.dart';\nimport 'package:geolocator/geolocator.dart';\n" + content

# 2. Local controllers init in showEditInstituteDialog
old_local_controllers = """  final nameController = TextEditingController(text: institute.name);
  final locationController = TextEditingController(text: institute.location);
  final phoneController = TextEditingController(text: institute.managerPhone);
  final isDark = Theme.of(context).brightness == Brightness.dark;"""

new_local_controllers = """  final nameController = TextEditingController(text: institute.name);
  final locationController = TextEditingController(text: institute.location);
  final phoneController = TextEditingController(text: institute.managerPhone);
  final latitudeController = TextEditingController(text: institute.latitude?.toString() ?? '');
  final longitudeController = TextEditingController(text: institute.longitude?.toString() ?? '');
  final isDark = Theme.of(context).brightness == Brightness.dark;"""

content = content.replace(old_local_controllers, new_local_controllers)

# 3. Add local map helpers inside showEditInstituteDialog
old_is_dark_line = """  final isDark = Theme.of(context).brightness == Brightness.dark;

  final RxList<String> selectedCategories = RxList<String>.from(
    institute.categoriesList,
  );"""

new_map_helpers = """  final isDark = Theme.of(context).brightness == Brightness.dark;

  final RxList<String> selectedCategories = RxList<String>.from(
    institute.categoriesList,
  );

  Future<void> _showMapDialog(LatLng startPoint) async {
    LatLng selectedPoint = startPoint;
    final MapController mapController = MapController();

    await showDialog(
      context: context,
      builder: (BuildContext context) {
        return StatefulBuilder(
          builder: (context, setDialogState) {
            Color dialogBg = isDark ? const Color(0xFF1E293B) : Colors.white;
            Color txtColor = isDark ? Colors.white : Colors.black87;
            Color subTxt = isDark ? Colors.white60 : Colors.black54;

            return Dialog(
              backgroundColor: dialogBg,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
              child: Container(
                width: 700,
                height: 550,
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'تحديد موقع المعهد على الخريطة',
                          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: txtColor),
                        ),
                        IconButton(
                          icon: Icon(Icons.close, color: txtColor),
                          onPressed: () => Navigator.pop(context),
                        )
                      ],
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'انقر فوق الخريطة لتحريك العلامة الحمراء 📍 إلى موقع معهدك بدقة، ثم اضغط على زر تأكيد الحفظ.',
                      style: TextStyle(fontSize: 12, color: subTxt),
                    ),
                    const SizedBox(height: 16),
                    Expanded(
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(12),
                        child: FlutterMap(
                          mapController: mapController,
                          options: MapOptions(
                            initialCenter: startPoint,
                            initialZoom: 15.0,
                            onTap: (tapPosition, point) {
                              setDialogState(() {
                                selectedPoint = point;
                              });
                            },
                          ),
                          children: [
                            TileLayer(
                              urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                              userAgentPackageName: 'com.msaar.admin',
                            ),
                            MarkerLayer(
                              markers: [
                                Marker(
                                  point: selectedPoint,
                                  width: 45,
                                  height: 45,
                                  child: const Icon(
                                    Icons.location_on_rounded,
                                    color: Colors.red,
                                    size: 45,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: [
                        TextButton(
                          onPressed: () => Navigator.pop(context),
                          child: const Text('إلغاء', style: TextStyle(color: Colors.grey)),
                        ),
                        const SizedBox(width: 16),
                        ElevatedButton(
                          onPressed: () {
                            latitudeController.text = selectedPoint.latitude.toString();
                            longitudeController.text = selectedPoint.longitude.toString();
                            Navigator.pop(context);
                            Get.snackbar(
                              'نجاح الاختيار',
                              'تم تعيين إحداثيات الموقع على الخريطة بنجاح!',
                              backgroundColor: AppColors.success,
                              colorText: Colors.white,
                            );
                          },
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppColors.primary,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                          ),
                          child: const Text('تأكيد اختيار الموقع'),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            );
          },
        );
      },
    );
  }

  Future<void> _getCurrentLocation() async {
    LatLng startPoint = const LatLng(15.35623, 44.19532); // Default to Sana'a Center
    
    double? currentLat = double.tryParse(latitudeController.text);
    double? currentLng = double.tryParse(longitudeController.text);
    if (currentLat != null && currentLng != null) {
      startPoint = LatLng(currentLat, currentLng);
    } else {
      try {
        bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
        if (serviceEnabled) {
          LocationPermission permission = await Geolocator.checkPermission();
          if (permission == LocationPermission.denied) {
            permission = await Geolocator.requestPermission();
          }
          if (permission == LocationPermission.whileInUse || permission == LocationPermission.always) {
            Position position = await Geolocator.getCurrentPosition(
              desiredAccuracy: LocationAccuracy.high
            );
            startPoint = LatLng(position.latitude, position.longitude);
          }
        }
      } catch (e) {
        debugPrint('Geolocator error: $e');
      }
    }
    
    await _showMapDialog(startPoint);
  }"""

content = content.replace(old_is_dark_line, new_map_helpers)

# 4. Insert Coordinates UI fields and Map button in the layout
old_layout_fields = """                            TextField(
                              controller: phoneController,
                              style: TextStyle(
                                color: isDark ? Colors.white : AppColors.textPrimary,
                              ),
                              decoration: InputDecoration(
                                labelText: 'رقم هاتف المدير',
                                labelStyle: TextStyle(
                                  color: isDark ? const Color(0xFF94A3B8) : null,
                                ),
                              ),
                            ),
                            const SizedBox(height: 20),"""

new_layout_fields = """                            TextField(
                              controller: phoneController,
                              style: TextStyle(
                                color: isDark ? Colors.white : AppColors.textPrimary,
                              ),
                              decoration: InputDecoration(
                                labelText: 'رقم هاتف المدير',
                                labelStyle: TextStyle(
                                  color: isDark ? const Color(0xFF94A3B8) : null,
                                ),
                              ),
                            ),
                            const SizedBox(height: 16),

                            // GPS Coordinates Display
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Text(
                                  'موقع المعهد الجغرافي (إحداثيات GPS)',
                                  style: TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 13,
                                    color: isDark ? Colors.white : AppColors.textPrimary,
                                  ),
                                ),
                                TextButton.icon(
                                  onPressed: _getCurrentLocation,
                                  icon: const Icon(Icons.map_rounded, size: 16, color: AppColors.primary),
                                  label: const Text(
                                    'عرض/تعديل على الخريطة',
                                    style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 12),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 8),
                            Row(
                              children: [
                                Expanded(
                                  child: TextField(
                                    controller: latitudeController,
                                    style: TextStyle(color: isDark ? Colors.white : AppColors.textPrimary),
                                    decoration: InputDecoration(
                                      labelText: 'خط العرض (Latitude)',
                                      labelStyle: TextStyle(color: isDark ? const Color(0xFF94A3B8) : null),
                                    ),
                                  ),
                                ),
                                const SizedBox(width: 16),
                                Expanded(
                                  child: TextField(
                                    controller: longitudeController,
                                    style: TextStyle(color: isDark ? Colors.white : AppColors.textPrimary),
                                    decoration: InputDecoration(
                                      labelText: 'خط الطول (Longitude)',
                                      labelStyle: TextStyle(color: isDark ? const Color(0xFF94A3B8) : null),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 20),"""

content = content.replace(old_layout_fields, new_layout_fields)

# 5. Pass coordinates in updateInstitute call
old_update_call = """                    bool success = await controller.updateInstitute(
                      institute.id,
                      nameController.text.trim(),
                      locationController.text.trim(),
                      phoneController.text.trim(),
                      selectedCategories.join(','),
                    );"""

new_update_call = """                    bool success = await controller.updateInstitute(
                      institute.id,
                      nameController.text.trim(),
                      locationController.text.trim(),
                      phoneController.text.trim(),
                      selectedCategories.join(','),
                      latitude: double.tryParse(latitudeController.text),
                      longitude: double.tryParse(longitudeController.text),
                    );"""

content = content.replace(old_update_call, new_update_call)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Super Admin Dialogs updated successfully with OSM maps support!")
