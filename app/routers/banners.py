import os
import shutil
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.tables import Banner
from pydantic import BaseModel
from typing import Optional
from app.core.cloudinary_config import upload_image_to_cloudinary

router = APIRouter()

UPLOAD_DIR = os.path.join("app", "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

class BannerCreate(BaseModel):
    title: str
    image_url: str
    category: str
    target_url: Optional[str] = ""
    is_active: Optional[bool] = True

class BannerUpdate(BaseModel):
    title: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    target_url: Optional[str] = None
    is_active: Optional[bool] = None

@router.post("/upload")
async def upload_banner_image(file: UploadFile = File(...)):
    # 1. Try uploading to Cloudinary
    try:
        cloudinary_url = upload_image_to_cloudinary(file.file, folder="banners")
        if cloudinary_url:
            return {"image_url": cloudinary_url}
    except Exception as cl_err:
        print(f"Cloudinary upload bypass to local fallback: {cl_err}")

    # 2. Local Fallback if Cloudinary is not configured or fails
    try:
        # Rewind the file stream in case it was read during Cloudinary attempt
        file.file.seek(0)
        filename = f"banner_{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"image_url": f"/static/uploads/{filename}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل رفع صورة الإعلان: {str(e)}"
        )

@router.get("/")
def get_banners(only_active: bool = False, db: Session = Depends(get_db)):
    query = db.query(Banner)
    if only_active:
        query = query.filter(Banner.is_active == True)
    banners = query.order_by(Banner.created_at.desc()).all()
    
    if not banners:
        return [
            {
                "id": "1",
                "title": "خصم 30% على كورس الإنجليزية المكثف",
                "image_url": "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?q=80&w=800&auto=format&fit=crop",
                "category": "discount",
                "target_url": "yali",
                "is_active": True
            },
            {
                "id": "2",
                "title": "افتتاح التسجيل لدورات الحاسوب لشهر أغسطس",
                "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=800&auto=format&fit=crop",
                "category": "news",
                "target_url": "telecom",
                "is_active": True
            }
        ]
        
    return [
        {
            "id": str(banner.id),
            "title": banner.title,
            "image_url": banner.image_url,
            "category": banner.category,
            "target_url": banner.target_url or "",
            "is_active": banner.is_active
        }
        for banner in banners
    ]

@router.post("/")
def create_banner(banner_data: BannerCreate, db: Session = Depends(get_db)):
    new_banner = Banner(
        title=banner_data.title,
        image_url=banner_data.image_url,
        category=banner_data.category,
        target_url=banner_data.target_url or "",
        is_active=banner_data.is_active if banner_data.is_active is not None else True
    )
    
    try:
        db.add(new_banner)
        db.commit()
        db.refresh(new_banner)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل إضافة الإعلان الترويجي: {str(e)}"
        )
        
    return {
        "id": str(new_banner.id),
        "title": new_banner.title,
        "image_url": new_banner.image_url,
        "category": new_banner.category,
        "target_url": new_banner.target_url or "",
        "is_active": new_banner.is_active
    }

@router.put("/{banner_id}/")
def update_banner(banner_id: str, banner_data: BannerUpdate, db: Session = Depends(get_db)):
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الإعلان غير موجود!"
        )
    if banner_data.title is not None:
        banner.title = banner_data.title
    if banner_data.image_url is not None:
        banner.image_url = banner_data.image_url
    if banner_data.category is not None:
        banner.category = banner_data.category
    if banner_data.target_url is not None:
        banner.target_url = banner_data.target_url
    if banner_data.is_active is not None:
        banner.is_active = banner_data.is_active
        
    try:
        db.commit()
        db.refresh(banner)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل تحديث الإعلان: {str(e)}"
        )
    return {
        "id": str(banner.id),
        "title": banner.title,
        "image_url": banner.image_url,
        "category": banner.category,
        "target_url": banner.target_url or "",
        "is_active": banner.is_active
    }

@router.delete("/{banner_id}/")
def delete_banner(banner_id: str, db: Session = Depends(get_db)):
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        return {"status": "success", "message": "Mock banner removed."}
        
    try:
        db.delete(banner)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل حذف الإعلان: {str(e)}"
        )
        
    return {"status": "success", "message": "Banner deleted successfully."}
