import re

file_path = r"C:\Users\alial\student\backend\app\routers\auth.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Locate login_institute and inject coordinates lookup at the start
old_logic = """def login_institute(credentials: InstituteLogin, db: Session = Depends(get_db)):
    # 1. Verify institute by slug or phone"""

new_logic = """def login_institute(credentials: InstituteLogin, db: Session = Depends(get_db)):
    # 1. Verify institute by slug or phone"""

# Find the user role return dict
old_user_dict = """                    "institute": {
                        "id": str(inst.id),
                        "name": inst.name,
                        "slug": inst.slug,
                        "category": inst.category or "",
                        "location": inst.location or "",
                        "jeep_number": inst.jeep_number or ""
                    }"""

new_user_dict = """                    "institute": {
                        "id": str(inst.id),
                        "name": inst.name,
                        "slug": inst.slug,
                        "category": inst.category or "",
                        "location": inst.location or "",
                        "jeep_number": inst.jeep_number or "",
                        "latitude": float(main_branch.latitude) if main_branch and main_branch.latitude is not None else None,
                        "longitude": float(main_branch.longitude) if main_branch and main_branch.longitude is not None else None
                    }"""

# Find the admin return dict
old_admin_dict = """        "institute": {
            "id": str(inst.id),
            "name": inst.name,
            "slug": inst.slug,
            "category": inst.category or "",
            "location": inst.location or "",
            "jeep_number": inst.jeep_number or ""
        }"""

new_admin_dict = """        "institute": {
            "id": str(inst.id),
            "name": inst.name,
            "slug": inst.slug,
            "category": inst.category or "",
            "location": inst.location or "",
            "jeep_number": inst.jeep_number or "",
            "latitude": float(main_branch.latitude) if main_branch and main_branch.latitude is not None else None,
            "longitude": float(main_branch.longitude) if main_branch and main_branch.longitude is not None else None
        }"""

# Inject branch lookup at start of login_institute
old_verify_inst = """    # 1. Verify institute by slug or phone
    if credentials.slug:
        inst = db.query(Institute).filter(Institute.slug == credentials.slug).first()
    else:
        inst = db.query(Institute).filter(Institute.manager_phone == credentials.phone).first()
        
    if not inst:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المعهد غير موجود بالنظام!"
        )"""

new_verify_inst = """    # 1. Verify institute by slug or phone
    if credentials.slug:
        inst = db.query(Institute).filter(Institute.slug == credentials.slug).first()
    else:
        inst = db.query(Institute).filter(Institute.manager_phone == credentials.phone).first()
        
    if not inst:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المعهد غير موجود بالنظام!"
        )
        
    # Fetch coordinates of the main branch
    from app.models.tables import InstituteBranch
    main_branch = db.query(InstituteBranch).filter(
        InstituteBranch.institute_id == inst.id,
        InstituteBranch.is_main_branch == True
    ).first()"""

content = content.replace(old_verify_inst, new_verify_inst)
content = content.replace(old_user_dict, new_user_dict)
content = content.replace(old_admin_dict, new_admin_dict)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Auth endpoint coordinates return added!")
