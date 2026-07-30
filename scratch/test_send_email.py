import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.email_helper import send_otp_email

email = "alialmaden.almaden@gmail.com"
code = "998877"
print(f"Sending test OTP email to {email}...")
success = send_otp_email(email, code)
print(f"Email sent successfully: {success}")
