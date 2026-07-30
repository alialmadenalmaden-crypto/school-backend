import re

file_path = r"C:\Users\alial\student\backend\app\routers\institutes.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update InstituteUpdate class definition
old_update_class = """class InstituteUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    logo_url: Optional[str] = None
    manager_phone: Optional[str] = None
    category: Optional[str] = None"""

new_update_class = """class InstituteUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    logo_url: Optional[str] = None
    manager_phone: Optional[str] = None
    category: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None"""

content = content.replace(old_update_class, new_update_class)

# 2. Update update_institute route logic
old_put_logic = """    if inst_data.manager_phone is not None:
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
    }"""

new_put_logic = """    if inst_data.manager_phone is not None:
        inst.manager_phone = inst_data.manager_phone
    if inst_data.category is not None:
        inst.category = inst_data.category
        
    # Update coordinates of the main branch
    from app.models.tables import InstituteBranch
    main_branch = db.query(InstituteBranch).filter(
        InstituteBranch.institute_id == inst.id,
        InstituteBranch.is_main_branch == True
    ).first()
    if main_branch:
        if inst_data.latitude is not None:
            main_branch.latitude = inst_data.latitude
        if inst_data.longitude is not None:
            main_branch.longitude = inst_data.longitude

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
        "is_active": inst.is_active,
        "latitude": float(main_branch.latitude) if main_branch and main_branch.latitude is not None else None,
        "longitude": float(main_branch.longitude) if main_branch and main_branch.longitude is not None else None
    }"""

content = content.replace(old_put_logic, new_put_logic)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("PUT institute endpoint supports coordinates updates now!")
