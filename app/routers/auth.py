from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.tables import Student, Institute, InstituteAdmin, SuperAdmin, User, Role, UserRole
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.email_helper import generate_and_save_otp, verify_saved_otp, send_otp_email

router = APIRouter()

class StudentRegister(BaseModel):
    full_name: str
    email: EmailStr
    phone: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "student"

class InstituteLogin(BaseModel):
    slug: str
    phone: str
    password: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_student(student: StudentRegister, db: Session = Depends(get_db)):
    # Clean phone number formats
    clean_phone = student.phone.strip()
    if not clean_phone.startswith("+"):
        if clean_phone.startswith("7") or clean_phone.startswith("0"):
            clean_phone = "+967" + clean_phone.lstrip("0")
        else:
            clean_phone = "+967" + clean_phone

    # Check if student already exists in legacy Student table or new User table
    existing_student = db.query(Student).filter(Student.email == student.email).first()
    existing_user = db.query(User).filter((User.email == student.email) | (User.phone == clean_phone)).first()
    
    if existing_student or existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="البريد الإلكتروني أو رقم الهاتف مسجل بالفعل!"
        )
        
    # 1. Create new student in legacy Student table (for backward compatibility)
    new_student = Student(
        full_name=student.full_name,
        email=student.email,
        phone=student.phone,
        is_email_verified=False
    )
    
    # 2. Create new user in the unified User table
    name_parts = student.full_name.strip().split()
    first_name = name_parts[0] if name_parts else student.full_name
    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
    
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=student.email,
        phone=clean_phone,
        password_hash=get_password_hash("student123"), # Default password fallback
        status="pending_verification"
    )
    
    try:
        db.add(new_student)
        db.add(new_user)
        db.flush() # Populate IDs
        
        # 3. Assign Student role
        student_role = db.query(Role).filter(Role.code == "student").first()
        if student_role:
            ur = UserRole(user_id=new_user.id, role_id=student_role.id)
            db.add(ur)
            
        db.commit()
        db.refresh(new_student)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل حفظ البيانات في قاعدة البيانات: {str(e)}"
        )
        
    # Generate OTP and send email
    code = generate_and_save_otp(student.email)
    send_otp_email(student.email, code)
    
    return {
        "status": "success",
        "message": "تم إنشاء الحساب بنجاح. أرسلنا رمز التحقق إلى بريدك الإلكتروني!",
        "student": {
            "id": str(new_student.id),
            "full_name": new_student.full_name,
            "email": new_student.email,
            "phone": new_student.phone
        }
    }

@router.post("/login")
@router.post("/login/")
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    if credentials.role == "super_admin":
        # First check the new User table with super_admin role
        user = db.query(User).filter(User.email == credentials.email).first()
        if user:
            # Verify role is super_admin
            role_assigned = db.query(UserRole).join(Role).filter(
                UserRole.user_id == user.id,
                Role.code.in_(["super_admin", "platform_admin"])
            ).first()
            
            if role_assigned and verify_password(credentials.password, user.password_hash):
                token = create_access_token(data={"sub": str(user.id), "role": "super_admin"})
                return {
                    "token": token,
                    "access_token": token,
                    "token_type": "bearer",
                    "name": f"{user.first_name} {user.last_name or ''}".strip(),
                    "email": user.email
                }
        
        # Legacy fallback
        admin = db.query(SuperAdmin).filter(SuperAdmin.email == credentials.email).first()
        if not admin or not verify_password(credentials.password, admin.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="البريد الإلكتروني أو كلمة المرور للمشرف غير صحيحة!"
            )
        
        token = create_access_token(data={"sub": str(admin.id), "role": "super_admin"})
        return {
            "token": token,
            "access_token": token,
            "token_type": "bearer",
            "name": admin.name,
            "email": admin.email
        }
        
    # Student login
    user = db.query(User).filter(User.email == credentials.email).first()
    if user:
        if user.status == "blocked" or user.status == "suspended":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="تم تجميد حسابك! يرجى التواصل مع إدارة المنصة."
            )
            
        token = create_access_token(data={"sub": str(user.id), "role": "student"})
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "name": f"{user.first_name} {user.last_name or ''}".strip()
            }
        }

    # Legacy student login fallback
    student = db.query(Student).filter(Student.email == credentials.email).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="البريد الإلكتروني أو كلمة المرور غير صحيحة!"
        )
        
    if not student.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="تم تجميد حسابك! يرجى التواصل مع إدارة المنصة."
        )
        
    token = create_access_token(data={"sub": str(student.id), "role": "student"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(student.id),
            "email": student.email,
            "name": student.full_name
        }
    }

@router.post("/verify-email")
def verify_email(email: str, code: str, db: Session = Depends(get_db)):
    if not verify_saved_otp(email, code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="رمز التحقق غير صحيح أو منتهي الصلاحية!"
        )
        
    # Verify legacy Student
    student = db.query(Student).filter(Student.email == email).first()
    if student:
        student.is_email_verified = True
        
    # Verify new User
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.status = "active"
        if not user.phone_verified_at:
            user.phone_verified_at = datetime.utcnow()
        user.email_verified_at = datetime.utcnow()
        
    db.commit()
    
    return {
        "status": "success",
        "message": "تم تفعيل الحساب بنجاح!"
    }

@router.post("/resend-code")
def resend_code(email: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == email).first()
    user = db.query(User).filter(User.email == email).first()
    
    if not student and not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الحساب غير موجود!"
        )
        
    code = generate_and_save_otp(email)
    send_otp_email(email, code)
    return {
        "status": "success",
        "message": "تم إعادة إرسال رمز التحقق بنجاح!"
    }

@router.post("/institute/login")
@router.post("/institute/login/")
def login_institute(credentials: InstituteLogin, db: Session = Depends(get_db)):
    # 1. Verify institute by slug
    inst = db.query(Institute).filter(Institute.slug == credentials.slug).first()
    if not inst:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المعرف اللفظي (Slug) للمعهد غير موجود بالنظام!"
        )
        
    # 2. Verify manager phone
    if inst.manager_phone != credentials.phone:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="رقم الموبايل للمدير غير صحيح لهذا المعهد!"
        )
        
    # 3. Verify admin password from legacy InstituteAdmin or new User
    # First search new User table linked to institute owner / admin role
    # Note: For MVP compatibility, we still search legacy InstituteAdmin
    admin = db.query(InstituteAdmin).filter(InstituteAdmin.institute_id == inst.id).first()
    if not admin or not verify_password(credentials.password, admin.password_hash):
        # Check new User associated via user_roles for this institute
        # Find any user with owner/admin role for this institute
        user_role = db.query(UserRole).join(Role).filter(
            UserRole.institute_id == inst.id,
            Role.code.in_(["institute_owner", "institute_admin"])
        ).first()
        
        if user_role:
            user = db.query(User).filter(User.id == user_role.user_id).first()
            if user and verify_password(credentials.password, user.password_hash):
                if user.status != "active":
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="هذا الحساب موقوف حالياً من قبل المشرف العام!"
                    )
                
                token = create_access_token(data={
                    "sub": str(user.id), 
                    "role": "institute_admin", 
                    "institute_id": str(inst.id)
                })
                return {
                    "status": "success",
                    "access_token": token,
                    "token_type": "bearer",
                    "admin": {
                        "id": str(user.id),
                        "name": f"{user.first_name} {user.last_name or ''}".strip(),
                        "email": user.email or "",
                    },
                    "institute": {
                        "id": str(inst.id),
                        "name": inst.name,
                        "slug": inst.slug,
                        "category": inst.category or "",
                        "location": inst.location or "",
                        "jeep_number": inst.jeep_number or ""
                    }
                }
                
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="كلمة المرور المدخلة غير صحيحة!"
        )
        
    if not inst.is_active or not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="هذا الحساب موقوف حالياً من قبل المشرف العام!"
        )
        
    token = create_access_token(data={"sub": str(admin.id), "role": "institute_admin", "institute_id": str(inst.id)})
    return {
        "status": "success",
        "access_token": token,
        "token_type": "bearer",
        "admin": {
            "id": str(admin.id),
            "name": admin.name,
            "email": admin.email,
        },
        "institute": {
            "id": str(inst.id),
            "name": inst.name,
            "slug": inst.slug,
            "category": inst.category or "",
            "location": inst.location or "",
            "jeep_number": inst.jeep_number or ""
        }
    }
