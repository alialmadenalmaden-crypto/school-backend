import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.email_helper import send_otp_email

email = "alialmadenalmaden@gmail.com"
code = "775533"
print(f"Sending test OTP email to {email}...")
success = send_otp_email(email, code)
print(f"Email sent outcome: {success}")
