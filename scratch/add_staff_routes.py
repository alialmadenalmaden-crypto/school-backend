import re

file_path = r"C:\Users\alial\student\backend\app\routers\institutes.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Append imports and routes
new_routes = """

# =========================================================================
# STAFF / MULTI-USER PERMISSIONS ROUTERS (طاقم عمل المعهد وصلاحياتهم)
# =========================================================================
from app.models.tables import InstituteAdmin

class StaffCreate(BaseModel):
    institute_id: str
    name: str
    email: str
    phone: str
    password: str
    role: str
    permissions: str

@router.get("/admin/staff/")
def get_staff_members(institute_id: str, db: Session = Depends(get_db)):
    staff = db.query(InstituteAdmin).filter(
        InstituteAdmin.institute_id == institute_id
    ).order_by(InstituteAdmin.created_at.desc()).all()
    return [
        {
            "id": str(s.id),
            "name": s.name,
            "email": s.email,
            "phone": s.phone or "",
            "role": s.role or "admin",
            "permissions": s.permissions or "all",
            "is_active": s.is_active
        }
        for s in staff
    ]

@router.post("/admin/staff/")
def add_staff_member(data: StaffCreate, db: Session = Depends(get_db)):
    # Check if email is already taken
    existing = db.query(InstituteAdmin).filter(InstituteAdmin.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="البريد الإلكتروني مسجل بالفعل لمستخدم آخر!")
    
    # Check if phone is already taken
    existing_phone = db.query(InstituteAdmin).filter(InstituteAdmin.phone == data.phone).first()
    if existing_phone:
        raise HTTPException(status_code=400, detail="رقم الموبايل مسجل بالفعل لمستخدم آخر!")
        
    from app.core.security import get_password_hash
    new_staff = InstituteAdmin(
        institute_id=data.institute_id,
        name=data.name,
        email=data.email,
        phone=data.phone,
        password_hash=get_password_hash(data.password),
        role=data.role,
        permissions=data.permissions,
        is_active=True
    )
    db.add(new_staff)
    try:
        db.commit()
        db.refresh(new_staff)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "success", "message": "تم إضافة العضو بنجاح!"}

@router.delete("/admin/staff/{staff_id}/")
def delete_staff_member(staff_id: str, db: Session = Depends(get_db)):
    staff = db.query(InstituteAdmin).filter(InstituteAdmin.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="العضو غير موجود!")
    db.delete(staff)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "success", "message": "تم حذف العضو بنجاح!"}
"""

content += new_routes

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Staff routes successfully appended to backend institutes.py!")
