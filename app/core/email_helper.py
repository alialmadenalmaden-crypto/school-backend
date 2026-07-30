import os
import json
import random
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

CODES_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "verification_codes.json")

def generate_and_save_otp(email: str) -> str:
    """Generates a 6-digit OTP and saves it to a local JSON file."""
    code = f"{random.randint(100000, 999999)}"
    
    # Load existing codes
    codes = {}
    if os.path.exists(CODES_FILE):
        try:
            with open(CODES_FILE, 'r', encoding='utf-8') as f:
                codes = json.load(f)
        except Exception:
            pass
            
    # Save the new code with a timestamp (expires in 15 minutes)
    codes[email] = {
        "code": code,
        "expires_at": (datetime.utcnow() + timedelta(minutes=15)).isoformat()
    }
    
    try:
        with open(CODES_FILE, 'w', encoding='utf-8') as f:
            json.dump(codes, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving OTP code to local JSON: {e}")
        
    return code

def verify_saved_otp(email: str, input_code: str) -> bool:
    """Verifies if the OTP code is correct and not expired."""

    if not os.path.exists(CODES_FILE):
        return False
        
    try:
        with open(CODES_FILE, 'r', encoding='utf-8') as f:
            codes = json.load(f)
    except Exception:
        return False
        
    if email not in codes:
        return False
        
    data = codes[email]
    saved_code = data.get("code")
    expires_at_str = data.get("expires_at")
    
    try:
        expires_at = datetime.fromisoformat(expires_at_str)
        if datetime.utcnow() > expires_at:
            # Expired
            return False
    except Exception:
        return False
        
    if saved_code == input_code:
        # Code matches, remove it
        try:
            del codes[email]
            with open(CODES_FILE, 'w', encoding='utf-8') as f:
                json.dump(codes, f, indent=4, ensure_ascii=False)
        except Exception:
            pass
        return True
        
    return False

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "email_config.json")

def send_otp_email(to_email: str, code: str) -> bool:
    """Sends a formatted HTML email with the verification OTP code."""
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; direction: rtl; text-align: right; background-color: #f7fafc; padding: 20px;">
        <div style="max-width: 500px; margin: auto; padding: 24px; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: #1e3a8a; margin: 0; font-size: 22px;">تطبيق مسار التعليمي</h2>
                <p style="color: #718096; font-size: 14px; margin-top: 5px;">رحلتك التعليمية تبدأ من هنا</p>
            </div>
            <hr style="border: 0; border-top: 1px solid #edf2f7; margin-bottom: 20px;">
            <p style="font-size: 15px; color: #2d3748; line-height: 1.6;">مرحباً بك في مسار،</p>
            <p style="font-size: 15px; color: #4a5568; line-height: 1.6;">رمز التحقق الخاص بك لإتمام عملية التسجيل وتفعيل الحساب هو:</p>
            
            <div style="font-size: 28px; font-weight: bold; text-align: center; color: #1e3a8a; background: #ebf8ff; padding: 16px; border: 1px dashed #bee3f8; border-radius: 12px; margin: 24px 0; letter-spacing: 5px;">
                {code}
            </div>
            
            <p style="font-size: 13px; color: #e53e3e; line-height: 1.6; font-weight: 500;">🚨 يرجى عدم مشاركة هذا الرمز مع أي شخص آخر لحماية أمن حسابك.</p>
            <hr style="border: 0; border-top: 1px solid #edf2f7; margin-top: 24px; margin-bottom: 20px;">
            <p style="font-size: 13px; color: #718096; line-height: 1.6; margin: 0;">شكراً لك،<br>فريق عمل تطبيق مسار</p>
        </div>
    </body>
    </html>
    """

    # 1. Try sending via Resend API Key
    resend_api_key = os.getenv("RESEND_API_KEY", "")
    if resend_api_key:
        import urllib.request
        import json
        try:
            url = "https://api.resend.com/emails"
            headers = {
                "Authorization": f"Bearer {resend_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "from": "Msaar App <onboarding@resend.dev>",
                "to": to_email,
                "subject": "رمز التحقق لتطبيق مسار التعليمي",
                "html": html_body
            }
            data_encoded = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data_encoded, headers=headers, method="POST")
            with urllib.request.urlopen(req) as response:
                print(f"RESEND EMAIL SUCCESS to {to_email}: {response.read().decode('utf-8')}")
                return True
        except Exception as e:
            print(f"RESEND EMAIL ERROR, falling back to SMTP: {e}")

    # 2. Fallback to standard SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "msaar.student@gmail.com"
    smtp_password = "antr klce mivp nmty"

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                smtp_server = config.get("smtp_server", smtp_server)
                smtp_port = config.get("smtp_port", smtp_port)
                smtp_username = config.get("smtp_username", smtp_username)
                smtp_password = config.get("smtp_password", "")
        except Exception:
            pass

    smtp_server = os.getenv("SMTP_SERVER", smtp_server)
    smtp_port = int(os.getenv("SMTP_PORT", str(smtp_port)))
    smtp_username = os.getenv("SMTP_USERNAME", smtp_username)
    smtp_password = os.getenv("SMTP_PASSWORD", smtp_password)
    if not smtp_password or "ضع_كلمة_مرور" in smtp_password:
        smtp_username = "msaar.student@gmail.com"
        smtp_password = "antr klce mivp nmty"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = "رمز التحقق لتطبيق مسار التعليمي"
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, msg.as_string())
        server.quit()
        print(f"SMTP EMAIL SENT SUCCESS to {to_email}")
        return True
    except Exception as smtp_err:
        print(f"SMTP EMAIL SENT ERROR to {to_email}: {smtp_err}")
        return False
