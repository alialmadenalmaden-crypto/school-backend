import re

file_path = r"C:\Users\alial\student\lib\pages\auth\verify_email_page.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace _buildCodeBox with a highly padded and centered text layout
old_build_code_box = """  Widget _buildCodeBox(int index, bool isDark) {
    return SizedBox(
      width: 46,
      child: TextField(
        controller: _controllers[index],
        focusNode: _focusNodes[index],
        maxLength: 1,
        textAlign: TextAlign.center,
        keyboardType: TextInputType.number,
        inputFormatters: [
          ArabicToEnglishNumbersFormatter(),
          FilteringTextInputFormatter.allow(RegExp(r'[0-9]')),
        ],
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
      width: 48,
      height: 56, // Enforce explicit height to fit the large text
      child: TextField(
        controller: _controllers[index],
        focusNode: _focusNodes[index],
        maxLength: 1,
        textAlign: TextAlign.center,
        textAlignVertical: TextAlignVertical.center, // Vertically center the digit
        keyboardType: TextInputType.number,
        inputFormatters: [
          ArabicToEnglishNumbersFormatter(),
          FilteringTextInputFormatter.allow(RegExp(r'[0-9]')),
        ],
        style: TextStyle(
          fontSize: 22,
          fontWeight: FontWeight.bold,
          fontFamily: 'sans-serif', // Use system font to ensure clean digits rendering
          color: isDark ? Colors.white : AppColors.textPrimary,
        ),
        decoration: InputDecoration(
          counterText: '',
          filled: true,
          fillColor: isDark ? Colors.white10 : Colors.grey.shade100,
          contentPadding: EdgeInsets.zero, // Remove default padding to prevent clipping
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

content = content.replace(old_build_code_box, new_build_code_box)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("verify_email_page.dart updated to prevent clipping/truncation in code boxes!")
