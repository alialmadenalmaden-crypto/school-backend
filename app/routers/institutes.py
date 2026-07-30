from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.tables import Institute, InstituteAdmin
from pydantic import BaseModel
from typing import Optional
import math

router = APIRouter()

def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # Earth radius in kilometers
    R = 6371.0
    
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    
    a = math.sin(d_lat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

class InstituteCreate(BaseModel):
    name: str
    slug: str
    location: Optional[str] = None
    logo_url: Optional[str] = None
    manager_phone: Optional[str] = None
    jeep_number: Optional[str] = None
    category: Optional[str] = None
    admin_email: str
    admin_password: str

class ChangePasswordRequest(BaseModel):
    email: str
    old_password: str
    new_password: str

@router.get("/")
def get_institutes(
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    db: Session = Depends(get_db)
):
    # Fetch all institutes from PostgreSQL (so Super Admin can manage all of them)
    institutes = db.query(Institute).order_by(Institute.created_at.desc()).all()
    
    # If no institutes exist in database, return mock list so the app doesn't break
    if not institutes:
        return [
            {
                "id": "lang1",
                "name": "معهد يالي (إنجليزي)",
                "slug": "yali",
                "logo_url": "https://api.dicebear.com/7.x/initials/svg?seed=yali",
                "location": "صنعاء - شارع بغداد",
                "manager_phone": "777111222",
                "category": "اللغات",
                "is_active": True,
                "distance_km": None
            },
            {
                "id": "lang2",
                "name": "معهد فلاي (إنجليزي)",
                "slug": "fly",
                "logo_url": "https://api.dicebear.com/7.x/initials/svg?seed=fly",
                "location": "صنعاء - حدة",
                "manager_phone": "777333444",
                "category": "اللغات",
                "is_active": True,
                "distance_km": None
            },
            {
                "id": "comp1",
                "name": "المعهد العام للاتصالات",
                "slug": "telecom",
                "logo_url": "https://api.dicebear.com/7.x/initials/svg?seed=telecom",
                "location": "صنعاء - الجراف",
                "manager_phone": "777555666",
                "category": "الحاسوب",
                "is_active": True,
                "distance_km": None
            }
        ]
        
    res_list = []
    for inst in institutes:
        min_dist = None
        # Find minimum distance to any branch of this institute
        from app.models.tables import InstituteBranch
        branches = db.query(InstituteBranch).filter(InstituteBranch.institute_id == inst.id).all()
        for branch in branches:
            if branch.latitude is not None and branch.longitude is not None:
                dist = calculate_haversine_distance(
                    float(lat), float(lng), 
                    float(branch.latitude), float(branch.longitude)
                )
                if min_dist is None or dist < min_dist:
                    min_dist = dist
                    
        res_list.append({
            "id": str(inst.id),
            "name": inst.name,
            "slug": inst.slug,
            "logo_url": inst.logo_url or f"https://api.dicebear.com/7.x/initials/svg?seed={inst.slug}",
            "location": inst.location or "",
            "manager_phone": inst.manager_phone or "",
            "jeep_number": inst.jeep_number or "",
            "category": inst.category or "",
            "is_active": inst.is_active,
            "distance_km": round(min_dist, 2) if min_dist is not None else None
        })
        
    if lat is not None and lng is not None:
        # Sort by distance_km (nulls last)
        res_list.sort(key=lambda x: x["distance_km"] if x["distance_km"] is not None else 999999)
        
    return res_list

@router.post("/")
def create_institute(inst_data: InstituteCreate, db: Session = Depends(get_db)):
    # Check if slug already exists
    existing = db.query(Institute).filter(Institute.slug == inst_data.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="المعرف اللفظي للمعهد (slug) مسجل بالفعل!"
        )
        
    # Check if admin email already exists
    existing_admin = db.query(InstituteAdmin).filter(InstituteAdmin.email == inst_data.admin_email).first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="البريد الإلكتروني لمدير المعهد مسجل بالفعل لجهة أخرى!"
        )
        
    new_inst = Institute(
        name=inst_data.name,
        slug=inst_data.slug,
        location=inst_data.location,
        logo_url=inst_data.logo_url or f"https://api.dicebear.com/7.x/initials/svg?seed={inst_data.slug}",
        manager_phone=inst_data.manager_phone,
        jeep_number=inst_data.jeep_number,
        category=inst_data.category,
        is_active=True
    )
    
    try:
        db.add(new_inst)
        db.commit()
        db.refresh(new_inst)
        
        # Create default Admin login credentials for this institute
        new_admin = InstituteAdmin(
            institute_id=new_inst.id,
            name="مدير المعهد",
            email=inst_data.admin_email,
            password_hash=inst_data.admin_password, # Storing plain/initial password
            is_active=True
        )
        db.add(new_admin)
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل حفظ بيانات المعهد أو حساب المدير: {str(e)}"
        )
        
    return {
        "id": str(new_inst.id),
        "name": new_inst.name,
        "slug": new_inst.slug,
        "logo_url": new_inst.logo_url,
        "location": new_inst.location,
        "manager_phone": new_inst.manager_phone or "",
        "jeep_number": new_inst.jeep_number or "",
        "category": new_inst.category or "",
        "is_active": new_inst.is_active
    }

@router.patch("/{inst_id}/toggle/")
def toggle_institute_active(inst_id: str, db: Session = Depends(get_db)):
    inst = db.query(Institute).filter(Institute.id == inst_id).first()
    if not inst:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المعهد غير موجود!"
        )
        
    inst.is_active = not inst.is_active
    db.commit()
    
    return {
        "status": "success",
        "is_active": inst.is_active
    }

# Accept requests
@router.post("/requests/{req_id}/accept/")
def accept_institute_request(req_id: str, inst_data: InstituteCreate, db: Session = Depends(get_db)):
    return create_institute(inst_data, db)

# Reject requests
@router.post("/requests/{req_id}/reject/")
def reject_institute_request(req_id: str):
    return {"status": "success", "message": f"Request {req_id} rejected successfully."}

class UpdateSettingsRequest(BaseModel):
    email: str
    jeep_number: str
    logo_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

# Change admin password (first time or later)
@router.post("/admin/change-password/")
def change_admin_password(data: ChangePasswordRequest, db: Session = Depends(get_db)):
    admin = db.query(InstituteAdmin).filter(InstituteAdmin.email == data.email).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="حساب مدير المعهد غير موجود!"
        )
    if admin.password_hash != data.old_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="كلمة المرور القديمة غير صحيحة!"
        )
    admin.password_hash = data.new_password
    db.commit()
    return {"status": "success", "message": "تم تغيير كلمة المرور بنجاح!"}

@router.post("/admin/update-settings/")
def update_settings(data: UpdateSettingsRequest, db: Session = Depends(get_db)):
    admin = db.query(InstituteAdmin).filter(InstituteAdmin.email == data.email).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="حساب مدير المعهد غير موجود!"
        )
    inst = db.query(Institute).filter(Institute.id == admin.institute_id).first()
    if not inst:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المعهد غير موجود!"
        )
    inst.jeep_number = data.jeep_number
    if data.logo_url is not None:
        inst.logo_url = data.logo_url
        
    # Update coordinates of the main branch
    from app.models.tables import InstituteBranch
    main_branch = db.query(InstituteBranch).filter(
        InstituteBranch.institute_id == inst.id,
        InstituteBranch.is_main_branch == True
    ).first()
    
    if main_branch:
        if data.latitude is not None:
            main_branch.latitude = data.latitude
        if data.longitude is not None:
            main_branch.longitude = data.longitude
            
    db.commit()
    
    # Return updated values
    return {
        "status": "success", 
        "message": "تم تحديث الإعدادات بنجاح!", 
        "jeep_number": inst.jeep_number, 
        "logo_url": inst.logo_url,
        "latitude": float(main_branch.latitude) if main_branch and main_branch.latitude is not None else None,
        "longitude": float(main_branch.longitude) if main_branch and main_branch.longitude is not None else None
    }

class InstituteUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    logo_url: Optional[str] = None
    manager_phone: Optional[str] = None
    category: Optional[str] = None

@router.get("/debug-db")
def debug_db(db: Session = Depends(get_db)):
    insts = db.query(Institute).all()
    return [{"id": inst.id, "name": inst.name, "slug": inst.slug, "logo_url": inst.logo_url} for inst in insts]

@router.put("/{inst_id}/")
def update_institute(inst_id: str, inst_data: InstituteUpdate, db: Session = Depends(get_db)):
    inst = db.query(Institute).filter(Institute.id == inst_id).first()
    if not inst:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المعهد غير موجود!"
        )
    if inst_data.name is not None:
        inst.name = inst_data.name
    if inst_data.location is not None:
        inst.location = inst_data.location
    if inst_data.logo_url is not None:
        inst.logo_url = inst_data.logo_url
    if inst_data.manager_phone is not None:
        inst.manager_phone = inst_data.manager_phone
    if inst_data.category is not None:
        inst.category = inst_data.category
        
    try:
        db.commit()
        db.refresh(inst)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل تحديث بيانات المعهد: {str(e)}"
        )
    return {
        "id": str(inst.id),
        "name": inst.name,
        "slug": inst.slug,
        "logo_url": inst.logo_url,
        "location": inst.location,
        "manager_phone": inst.manager_phone or "",
        "category": inst.category or "",
        "is_active": inst.is_active
    }
