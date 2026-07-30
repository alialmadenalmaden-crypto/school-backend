import re

file_path = r"C:\Users\alial\student\backend\app\routers\auth.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace verification and return logic in login_institute
old_login_block = """    # 2. Verify manager phone
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
                        "jeep_number": inst.jeep_number or "",
                        "latitude": float(main_branch.latitude) if main_branch and main_branch.latitude is not None else None,
                        "longitude": float(main_branch.longitude) if main_branch and main_branch.longitude is not None else None
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
            "jeep_number": inst.jeep_number or "",
            "latitude": float(main_branch.latitude) if main_branch and main_branch.latitude is not None else None,
            "longitude": float(main_branch.longitude) if main_branch and main_branch.longitude is not None else None
        }
    }"""

new_login_block = """    # 2. Verify login by checking InstituteAdmin with the phone first (supports multiple staff)
    admin = db.query(InstituteAdmin).filter(
        InstituteAdmin.institute_id == inst.id,
        InstituteAdmin.phone == credentials.phone
    ).first()
    
    # Fallback to check first admin in the institute if manager phone matches
    if not admin and inst.manager_phone == credentials.phone:
        admin = db.query(InstituteAdmin).filter(InstituteAdmin.institute_id == inst.id).first()
        
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="رقم الموبايل المدخل غير مسجل لهذا المعهد!"
        )
        
    # 3. Verify password
    if not verify_password(credentials.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="كلمة المرور المدخلة غير صحيحة!"
        )
        
    if not inst.is_active or not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="هذا الحساب موقوف حالياً!"
        )
        
    # Return user details, role, and permissions
    token = create_access_token(data={
        "sub": str(admin.id), 
        "role": getattr(admin, 'role', 'admin') or 'admin', 
        "institute_id": str(inst.id)
    })
    return {
        "status": "success",
        "access_token": token,
        "token_type": "bearer",
        "admin": {
            "id": str(admin.id),
            "name": admin.name,
            "email": admin.email,
            "role": getattr(admin, 'role', 'admin') or 'admin',
            "permissions": getattr(admin, 'permissions', 'all') or 'all'
        },
        "institute": {
            "id": str(inst.id),
            "name": inst.name,
            "slug": inst.slug,
            "category": inst.category or "",
            "location": inst.location or "",
            "jeep_number": inst.jeep_number or "",
            "latitude": float(main_branch.latitude) if main_branch and main_branch.latitude is not None else None,
            "longitude": float(main_branch.longitude) if main_branch and main_branch.longitude is not None else None
        }
    }"""

content = content.replace(old_login_block, new_login_block)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Backend auth login updated successfully to support staff login!")
