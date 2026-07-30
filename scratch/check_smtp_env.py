import re

file_path = r"C:\Users\alial\student\backend\app\main.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Append debug endpoint before the last line
debug_endpoint = """

@app.get("/api/smtp-debug")
def smtp_debug():
    import os
    from app.core.email_helper import CONFIG_FILE, send_otp_email
    import json
    
    file_exists = os.path.exists(CONFIG_FILE)
    file_content = {}
    if file_exists:
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                file_content = json.load(f)
                if "smtp_password" in file_content:
                    file_content["smtp_password"] = "SET (LENGTH: " + str(len(file_content["smtp_password"])) + ")"
        except Exception as e:
            file_content = {"error": str(e)}
            
    env_password = os.getenv("SMTP_PASSWORD", "")
    env_password_masked = "NOT_SET"
    if env_password:
        env_password_masked = f"SET (LENGTH: {len(env_password)}, STARTS_WITH: {env_password[:4]}, CONTAINS_TEMPLATE_TEXT: {'ضع_كلمة_مرور' in env_password})"
        
    return {
        "file_exists": file_exists,
        "file_path": CONFIG_FILE,
        "file_config": file_content,
        "env_username": os.getenv("SMTP_USERNAME", "NOT_SET"),
        "env_password_masked": env_password_masked,
        "default_username": "msaar.student@gmail.com"
    }
"""

content += debug_endpoint

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Temporary SMTP debug endpoint appended to main.py!")
