import re

file_path = r"C:\Users\alial\student\backend\app\routers\auth.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add BackgroundTasks import from fastapi if not present
if "from fastapi import" in content:
    content = content.replace("from fastapi import", "from fastapi import BackgroundTasks,")
else:
    content = "from fastapi import BackgroundTasks\n" + content

# 2. Update register_student signature and call
old_register_def = """def register_student(student: StudentRegister, db: Session = Depends(get_db)):"""
new_register_def = """def register_student(student: StudentRegister, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):"""

content = content.replace(old_register_def, new_register_def)

old_register_send = """    # Generate OTP and send email
    code = generate_and_save_otp(student.email)
    send_otp_email(student.email, code)"""

new_register_send = """    # Generate OTP and send email asynchronously in background
    code = generate_and_save_otp(student.email)
    background_tasks.add_task(send_otp_email, student.email, code)"""

content = content.replace(old_register_send, new_register_send)

# 3. Update resend_code signature and call
old_resend_def = """def resend_code(email: str, db: Session = Depends(get_db)):"""
new_resend_def = """def resend_code(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):"""

content = content.replace(old_resend_def, new_resend_def)

old_resend_send = """    code = generate_and_save_otp(email)
    send_otp_email(email, code)"""

new_resend_send = """    code = generate_and_save_otp(email)
    background_tasks.add_task(send_otp_email, email, code)"""

content = content.replace(old_resend_send, new_resend_send)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Backend registration and resend endpoints updated to send emails asynchronously in the background!")
