import re

file_path = r"C:\Users\alial\super_admin_desktop\lib\pages\dashboard\dialogs\institute_dialogs.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Locate the Row and replace it with Expanded Text
old_row = """                            Row(
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
                            ),"""

new_row = """                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Expanded(
                                  child: Text(
                                    'موقع المعهد الجغرافي (إحداثيات GPS)',
                                    style: TextStyle(
                                      fontWeight: FontWeight.bold,
                                      fontSize: 12,
                                      color: isDark ? Colors.white : AppColors.textPrimary,
                                    ),
                                    maxLines: 1,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                ),
                                TextButton.icon(
                                  onPressed: _getCurrentLocation,
                                  icon: const Icon(Icons.map_rounded, size: 14, color: AppColors.primary),
                                  label: const Text(
                                    'عرض/تعديل على الخريطة',
                                    style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 11),
                                  ),
                                ),
                              ],
                            ),"""

content = content.replace(old_row, new_row)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Super Admin overflow layout fixed successfully!")
