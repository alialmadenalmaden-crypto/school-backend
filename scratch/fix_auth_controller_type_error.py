import re

file_path = r"C:\Users\alial\student\lib\controllers\auth_controller.dart"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Helper function to get error message safely
safe_error_extractor_helper = """  String _getErrorMessage(dynamic responseData, String defaultMsg) {
    if (responseData == null) return defaultMsg;
    if (responseData is Map) {
      final detail = responseData['detail'];
      if (detail == null) return defaultMsg;
      if (detail is String) return detail;
      if (detail is List && detail.isNotEmpty) {
        final firstError = detail[0];
        if (firstError is Map && firstError.containsKey('msg')) {
          return firstError['msg'].toString();
        }
      }
      return detail.toString();
    }
    if (responseData is String && responseData.isNotEmpty) {
      if (responseData.trim().startsWith("<")) return defaultMsg;
      return responseData;
    }
    return defaultMsg;
  }"""

# Insert the helper inside the class
content = content.replace("class StudentAuthController extends GetxController {", "class StudentAuthController extends GetxController {\n" + safe_error_extractor_helper + "\n")

# 1. Update registerStudent catch block
old_register_catch = """    } catch (e) {
      if (e is DioException && e.response != null) {
        lastErrorMessage.value = e.response?.data['detail'] ?? 'حدث خطأ أثناء التسجيل';
      } else {
        lastErrorMessage.value = 'خطأ في الاتصال بالخادم! تأكد من تشغيل السيرفر.';
      }
    }"""

new_register_catch = """    } catch (e) {
      if (e is DioException && e.response != null) {
        lastErrorMessage.value = _getErrorMessage(e.response?.data, 'حدث خطأ أثناء التسجيل');
      } else {
        lastErrorMessage.value = 'خطأ في الاتصال بالخادم! تأكد من تشغيل السيرفر.';
      }
    }"""

content = content.replace(old_register_catch, new_register_catch)

# 2. Update verifyEmail catch block
old_verify_catch = """    } catch (e) {
      if (e is DioException && e.response != null) {
        lastErrorMessage.value = e.response?.data['detail'] ?? 'رمز التحقق غير صحيح!';
      } else {
        lastErrorMessage.value = 'خطأ في الاتصال بالخادم!';
      }
    }"""

new_verify_catch = """    } catch (e) {
      if (e is DioException && e.response != null) {
        lastErrorMessage.value = _getErrorMessage(e.response?.data, 'رمز التحقق غير صحيح!');
      } else {
        lastErrorMessage.value = 'خطأ في الاتصال بالخادم!';
      }
    }"""

content = content.replace(old_verify_catch, new_verify_catch)

# 3. Update resendCode catch block
old_resend_catch = """    } catch (e) {
      if (e is DioException && e.response != null) {
        Get.snackbar('خطأ', e.response?.data['detail'] ?? 'فشل إعادة الإرسال!');
      } else {
        Get.snackbar('خطأ', 'خطأ في الاتصال بالخادم!');
      }
    }"""

new_resend_catch = """    } catch (e) {
      if (e is DioException && e.response != null) {
        Get.snackbar('خطأ', _getErrorMessage(e.response?.data, 'فشل إعادة الإرسال!'));
      } else {
        Get.snackbar('خطأ', 'خطأ في الاتصال بالخادم!');
      }
    }"""

content = content.replace(old_resend_catch, new_resend_catch)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Unsafe error parsing crash (TypeError) fixed successfully in StudentAuthController!")
