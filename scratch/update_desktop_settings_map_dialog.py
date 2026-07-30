import re

file_path = r"C:\Users\alial\institute_desktop\lib\pages\settings\settings_page.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add latlong2 import at the top
content = "import 'package:latlong2/latlong2.dart';\n" + content

# 2. Locate _getCurrentLocation and rewrite it with map dialog
old_get_location = """  Future<void> _getCurrentLocation() async {
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
  }"""

new_get_location_and_dialog = """  Future<void> _showMapDialog(LatLng startPoint) async {
    LatLng selectedPoint = startPoint;
    final MapController mapController = MapController();

    await showDialog(
      context: context,
      builder: (BuildContext context) {
        return StatefulBuilder(
          builder: (context, setDialogState) {
            bool isDark = Theme.of(context).brightness == Brightness.dark;
            Color dialogBg = isDark ? const Color(0xFF1E1E2E) : Colors.white;
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
                              userAgentPackageName: 'com.msaar.institute',
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
                            setState(() {
                              _latitudeController.text = selectedPoint.latitude.toString();
                              _longitudeController.text = selectedPoint.longitude.toString();
                            });
                            Navigator.pop(context);
                            Get.snackbar(
                              'نجاح الاختيار',
                              'تم تعيين إحداثيات موقعك على الخريطة بنجاح!',
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
    
    // If coordinates already loaded/saved, open maps at that point!
    double? currentLat = double.tryParse(_latitudeController.text);
    double? currentLng = double.tryParse(_longitudeController.text);
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
        debugPrint('Geolocator helper error: $e');
      }
    }
    
    await _showMapDialog(startPoint);
  }"""

content = content.replace(old_get_location, new_get_location_and_dialog)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Interactive OSM map dialog integrated in desktop settings page!")
