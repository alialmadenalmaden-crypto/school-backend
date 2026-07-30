import re

file_path = r"C:\Users\alial\student\lib\pages\auth\verify_email_page.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add services.dart import
content = "import 'package:flutter/services.dart';\n" + content

# 2. Append the formatter class at the end of the file
formatter_class_code = """

class ArabicToEnglishNumbersFormatter extends TextInputFormatter {
  @override
  TextEditingValue formatEditUpdate(TextEditingValue oldValue, TextEditingValue newValue) {
    String text = newValue.text;
    text = text
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
    return newValue.copyWith(
      text: text,
      selection: TextSelection.collapsed(offset: text.length),
    );
  }
}
"""

content += formatter_class_code

# 3. Update _buildCodeBox TextField to use the formatter and clean up onChanged
old_textfield_block = """  Widget _buildCodeBox(int index, bool isDark) {
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

new_textfield_block = """  Widget _buildCodeBox(int index, bool isDark) {
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

content = content.replace(old_textfield_block, new_textfield_block)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("verify_email_page.dart updated with ArabicToEnglishNumbersFormatter successfully!")
