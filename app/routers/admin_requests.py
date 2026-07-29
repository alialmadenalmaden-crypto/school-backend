import os
import uuid
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.tables import SuperAdminRequest, Banner, Category, Institute
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

class RequestCreate(BaseModel):
    institute_id: str
    request_type: str # ad, category, support
    title: Optional[str] = None
    details: Optional[str] = None
    image_url: Optional[str] = None

@router.post("/upload-image/")
def upload_image(request: Request, file: UploadFile = File(...)):
    # Create uploads directory under static
    upload_dir = os.path.join("app", "static", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename to prevent collision
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل حفظ الصورة المرفوعة: {str(e)}"
        )
        
    # Return the dynamic server URL
    base_url = str(request.base_url).rstrip('/')
    return {"url": f"{base_url}/static/uploads/{filename}"}

@router.post("/")
def create_request(req_data: RequestCreate, db: Session = Depends(get_db)):
    # Validate institute exists
    inst = None
    try:
        uuid.UUID(req_data.institute_id)
        inst = db.query(Institute).filter(Institute.id == req_data.institute_id).first()
    except ValueError:
        pass

    if not inst:
        inst = db.query(Institute).filter(Institute.slug == req_data.institute_id).first()
        if not inst:
            inst = db.query(Institute).first()
            if not inst:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="لم يتم العثور على المعهد المنسوب إليه الطلب."
                )

    new_request = SuperAdminRequest(
        institute_id=inst.id,
        request_type=req_data.request_type,
        title=req_data.title,
        details=req_data.details,
        image_url=req_data.image_url,
        status="pending"
    )
    
    try:
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل إرسال الطلب: {str(e)}"
        )
        
    return {
        "id": str(new_request.id),
        "institute_id": str(new_request.institute_id),
        "request_type": new_request.request_type,
        "title": new_request.title,
        "details": new_request.details,
        "image_url": new_request.image_url,
        "status": new_request.status,
        "created_at": new_request.created_at.isoformat()
    }

@router.get("/")
def get_requests(status_filter: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(SuperAdminRequest)
    if status_filter:
        query = query.filter(SuperAdminRequest.status == status_filter)
    
    requests = query.order_by(SuperAdminRequest.created_at.desc()).all()
    
    return [
        {
            "id": str(r.id),
            "institute_id": str(r.institute_id),
            "institute_name": r.institute.name if r.institute else "معهد غير معروف",
            "institute_slug": r.institute.slug if r.institute else "",
            "request_type": r.request_type,
            "title": r.title,
            "details": r.details,
            "image_url": r.image_url,
            "status": r.status,
            "created_at": r.created_at.isoformat()
        }
        for r in requests
    ]

@router.patch("/{request_id}/approve/")
def approve_request(request_id: str, db: Session = Depends(get_db)):
    req = db.query(SuperAdminRequest).filter(SuperAdminRequest.id == request_id).first()
    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الطلب غير موجود في النظام."
        )
        
    if req.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="تمت معالجة هذا الطلب مسبقاً."
        )
        
    try:
        # Perform action based on request type
        if req.request_type == "ad":
            # Add to banners
            new_banner = Banner(
                title=req.title,
                image_url=req.image_url or "",
                category="news",
                target_url=req.institute.slug if req.institute else ""
            )
            db.add(new_banner)
            
        elif req.request_type == "category":
            # Add to categories
            new_cat = Category(
                name_ar=req.title,
                name_en=req.details or "New Category",
                icon="school"
            )
            db.add(new_cat)
            
        # Update request status
        req.status = "approved"
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل إقرار الطلب وتحديث النظام: {str(e)}"
        )
        
    return {"status": "success", "message": "تمت الموافقة على الطلب بنجاح وتحديث النظام."}

@router.patch("/{request_id}/reject/")
def reject_request(request_id: str, db: Session = Depends(get_db)):
    req = db.query(SuperAdminRequest).filter(SuperAdminRequest.id == request_id).first()
    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الطلب غير موجود في النظام."
        )
        
    if req.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="تمت معالجة هذا الطلب مسبقاً."
        )
        
    try:
        req.status = "rejected"
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل رفض الطلب: {str(e)}"
        )
        
    return {"status": "success", "message": "تم رفض الطلب واستبعاد التعديلات."}
