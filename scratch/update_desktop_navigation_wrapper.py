import re

file_path = r"C:\Users\alial\institute_desktop\lib\pages\navigation_wrapper.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add import
content = "import 'staff/manage_staff_page.dart';\n" + content

# 2. Update _pages list
old_pages = """  final List<Widget> _pages = [
    const DashboardPage(),
    const ManageCoursesPage(),
    const ManageBookingsPage(),
    const ManageStudentsPage(),
    const SettingsPage(),
  ];"""

new_pages = """  final List<Widget> _pages = [
    const DashboardPage(),
    const ManageCoursesPage(),
    const ManageBookingsPage(),
    const ManageStudentsPage(),
    const ManageStaffPage(),
    const SettingsPage(),
  ];"""

content = content.replace(old_pages, new_pages)

# 3. Update build menu items with roles and permissions checks
old_menu_items = """                      // Menu Items
                      _buildMenuItem(
                        icon: Icons.dashboard_outlined,
                        label: 'الرئيسية',
                        index: 0,
                      ),
                      _buildMenuItem(
                        icon: Icons.menu_book_rounded,
                        label: 'إدارة الكورسات',
                        index: 1,
                      ),
                      _buildMenuItem(
                        icon: Icons.assignment_turned_in_outlined,
                        label: 'طلبات الحجز',
                        index: 2,
                      ),
                      _buildMenuItem(
                        icon: Icons.people_alt_rounded,
                        label: 'إدارة الطلاب',
                        index: 3,
                      ),
                      _buildMenuItem(
                        icon: Icons.settings_outlined,
                        label: 'الإعدادات',
                        index: 4,
                      ),"""

new_menu_items = """                      // Menu Items
                      _buildMenuItem(
                        icon: Icons.dashboard_outlined,
                        label: 'الرئيسية',
                        index: 0,
                      ),
                      
                      // Check permissions for courses
                      if (_authController.adminRole.value == 'admin' || _authController.adminPermissions.value.contains('courses'))
                        _buildMenuItem(
                          icon: Icons.menu_book_rounded,
                          label: 'إدارة الكورسات',
                          index: 1,
                        ),
                        
                      // Check permissions for bookings
                      if (_authController.adminRole.value == 'admin' || _authController.adminPermissions.value.contains('bookings'))
                        _buildMenuItem(
                          icon: Icons.assignment_turned_in_outlined,
                          label: 'طلبات الحجز',
                          index: 2,
                        ),
                        
                      // Check permissions for students
                      if (_authController.adminRole.value == 'admin' || _authController.adminPermissions.value.contains('students'))
                        _buildMenuItem(
                          icon: Icons.people_alt_rounded,
                          label: 'إدارة الطلاب',
                          index: 3,
                        ),
                        
                      // Only visible to admin/manager
                      if (_authController.adminRole.value == 'admin')
                        _buildMenuItem(
                          icon: Icons.badge_outlined,
                          label: 'طاقم العمل',
                          index: 4,
                        ),
                        
                      _buildMenuItem(
                        icon: Icons.settings_outlined,
                        label: 'الإعدادات',
                        index: 5,
                      ),"""

content = content.replace(old_menu_items, new_menu_items)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Navigation wrapper successfully updated in institute app with staff page and permission gating!")
