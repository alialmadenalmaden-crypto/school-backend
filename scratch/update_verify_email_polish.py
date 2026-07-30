import re

file_path = r"C:\Users\alial\student\lib\pages\auth\verify_email_page.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add _clearFields method
old_dispose = """  @override
  void dispose() {
    for (var c in _controllers) c.dispose();
    for (var f in _focusNodes) f.dispose();
    super.dispose();
  }"""

new_dispose = """  @override
  void dispose() {
    for (var c in _controllers) c.dispose();
    for (var f in _focusNodes) f.dispose();
    super.dispose();
  }

  void _clearFields() {
    setState(() {
      for (var c in _controllers) {
        c.clear();
      }
    });
    _focusNodes[0].requestFocus();
  }"""

content = content.replace(old_dispose, new_dispose)

# 2. Update Resend Code button action
old_resend_btn = """            TextButton(
              onPressed: () => _authController.resendCode(),
              child: const Text("""

new_resend_btn = """            TextButton(
              onPressed: () {
                _clearFields();
                _authController.resendCode();
              },
              child: const Text("""

content = content.replace(old_resend_btn, new_resend_btn)

# 3. Update style and onChanged in _buildCodeBox
old_build_code_box = """  Widget _buildCodeBox(int index, bool isDark) {
    return SizedBox(
      width: 46,
      child: TextField(
        controller: _controllers[index],
        focusNode: _focusNodes[index],
        maxLength: 1,
        textAlign: TextAlign.center,
        keyboardType: TextInputType.number,
        style: TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.bold,
          color: isDark ? Colors.white : AppColors.textPrimary,
        ),
        decoration: InputDecoration(
          counterText: '',
          filled: true,
          fillColor: isDark ? Colors.white10 : Colors.grey.shade100,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(color: isDark ? Colors.white24 : Colors.grey.shade300),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: AppColors.primary, width: 2),
          ),
        ),
        onChanged: (v) {
          if (v.isNotEmpty && index < 5) {
            _focusNodes[index + 1].requestFocus();
          } else if (v.isEmpty && index > 0) {
            _focusNodes[index - 1].requestFocus();
          }
        },
      ),
    );
  }"""

new_build_code_box = """  Widget _buildCodeBox(int index, bool isDark) {
    return SizedBox(
      width: 46,
      child: TextField(
        controller: _controllers[index],
        focusNode: _focusNodes[index],
        maxLength: 1,
        textAlign: TextAlign.center,
        keyboardType: TextInputType.number,
        style: TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.bold,
          fontFamily: 'sans-serif', // Use system font to ensure clean digits rendering
          color: isDark ? Colors.white : AppColors.textPrimary,
        ),
        decoration: InputDecoration(
          counterText: '',
          filled: true,
          fillColor: isDark ? Colors.white10 : Colors.grey.shade100,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(color: isDark ? Colors.white24 : Colors.grey.shade300),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: AppColors.primary, width: 2),
          ),
        ),
        onChanged: (v) {
          if (v.isNotEmpty) {
            // Convert Eastern Arabic numbers (٠-٩) to Western (0-9) dynamically
            String clean = v
                .replaceAll('٠', '0')
                .replaceAll('١', '1')
                .replaceAll('٢', '2')
                .replaceAll('٣', '3')
                .replaceAll('٤', '4')
                .replaceAll('٥', '5')
                .replaceAll('٦', '6')
                .replaceAll('٧', '7')
                .replaceAll('٨', '8')
                .replaceAll('٩', '9');
            if (clean != v) {
              _controllers[index].text = clean;
              _controllers[index].selection = TextSelection.fromPosition(
                TextPosition(offset: clean.length),
              );
            }
            if (index < 5) {
              _focusNodes[index + 1].requestFocus();
            }
          } else if (index > 0) {
            _focusNodes[index - 1].requestFocus();
          }
        },
      ),
    );
  }"""

content = content.replace(old_build_code_box, new_build_code_box)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("verify_email_page.dart polished successfully!")
