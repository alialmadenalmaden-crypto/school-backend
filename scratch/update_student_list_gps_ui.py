import re

file_path = r"C:\Users\alial\student\lib\pages\home\institutes_list_page.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update _getInstitutesByCategory to map distance_km field
old_map_inst = """      if (categoryId == 'all' || mappedIds.contains(categoryId) || matchesLanguage) {
        if (!list.any((item) => item['id'] == inst.id)) {
          list.add({
            'id': inst.id,
            'name': inst.name,
            'category': categoryId == 'all' ? mappedIds.first : categoryId,
            'location': locationStr.isNotEmpty ? locationStr : 'صنعاء',
            'price': 'متاح للتسجيل',
            'slug': inst.slug,
            'logo_url': inst.logoUrl,
          });
        }
      }"""

new_map_inst = """      if (categoryId == 'all' || mappedIds.contains(categoryId) || matchesLanguage) {
        if (!list.any((item) => item['id'] == inst.id)) {
          list.add({
            'id': inst.id,
            'name': inst.name,
            'category': categoryId == 'all' ? mappedIds.first : categoryId,
            'location': locationStr.isNotEmpty ? locationStr : 'صنعاء',
            'price': 'متاح للتسجيل',
            'slug': inst.slug,
            'logo_url': inst.logoUrl,
            'distance_km': inst.distanceKm,
          });
        }
      }"""

content = content.replace(old_map_inst, new_map_inst)

# 2. Update _onFilterTap to invoke sortByGPS or clearGpsFilter
old_filter_tap = """  void _onFilterTap(String filter) {
    setState(() => selectedFilter = filter);
  }"""

new_filter_tap = """  void _onFilterTap(String filter) async {
    setState(() => selectedFilter = filter);
    if (filter == 'الأقرب' || filter == 'Nearby') {
      await _institutesController.sortByGPS();
    } else {
      if (_institutesController.isGpsFilterActive.value) {
        await _institutesController.clearGpsFilter();
      }
    }
  }"""

content = content.replace(old_filter_tap, new_filter_tap)

# 3. Add Distance Badge in _buildInstituteCard
old_location_row = """              Row(
                children: [
                  const Icon(Icons.location_on_rounded, size: 14, color: Colors.grey),
                  SizedBox(width: 4.w),
                  Expanded(
                    child: Text(
                      data['location'] ?? 'بغداد',
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: TextStyle(fontSize: 12.sp, color: Colors.grey),
                    ),
                  ),
                ],
              ),"""

new_location_row = """              Row(
                children: [
                  const Icon(Icons.location_on_rounded, size: 14, color: Colors.grey),
                  SizedBox(width: 4.w),
                  Expanded(
                    child: Text(
                      data['location'] ?? 'بغداد',
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: TextStyle(fontSize: 12.sp, color: Colors.grey),
                    ),
                  ),
                  if (data['distance_km'] != null) ...[
                    SizedBox(width: 8.w),
                    Container(
                      padding: EdgeInsets.symmetric(horizontal: 6.w, vertical: 2.h),
                      decoration: BoxDecoration(
                        color: AppColors.primary.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(4.r),
                      ),
                      child: Text(
                        'على بعد ${data['distance_km']} كم',
                        style: TextStyle(
                          fontSize: 10.sp,
                          color: AppColors.primary,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ],
              ),"""

content = content.replace(old_location_row, new_location_row)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("GPS filtering UI integrated in student app!")
