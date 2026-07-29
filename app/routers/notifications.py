from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.db.session import get_db
from app.models.tables import Student, InstituteAdmin
from app.core.fcm_helper import send_broadcast_notification, send_topic_notification

router = APIRouter()

class TokenUpdateRequest(BaseModel):
    email: str
    token: str
    user_type: str # "student" or "admin"

class BroadcastRequest(BaseModel):
    target: str # "students", "institutes", or "all"
    title: str
    body: str

@router.post("/update-token/")
def update_token(data: TokenUpdateRequest, db: Session = Depends(get_db)):
    if data.user_type == "student":
        student = db.query(Student).filter(Student.email == data.email).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="طالب غير مسجل بهذا البريد الإلكتروني!"
            )
        student.fcm_token = data.token
        db.commit()
        return {"status": "success", "message": "تم تحديث رمز الإشعارات للطالب بنجاح!"}
    
    elif data.user_type == "admin":
        admin = db.query(InstituteAdmin).filter(InstituteAdmin.email == data.email).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="حساب مدير معهد غير مسجل بهذا البريد الإلكتروني!"
            )
        admin.fcm_token = data.token
        db.commit()
        return {"status": "success", "message": "تم تحديث رمز الإشعارات لمدير المعهد بنجاح!"}
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="نوع المستخدم غير صحيح! يجب أن يكون student أو admin"
        )

@router.post("/broadcast/")
def broadcast_notification(data: BroadcastRequest, db: Session = Depends(get_db)):
    if data.target == "all":
        # Send to the common topic "all_users"
        success = send_topic_notification("all_users", data.title, data.body)
        if success:
            return {
                "status": "success",
                "message": "تم إرسال الإشعار الجماعي لكافة الأجهزة (المسجلين وغير المسجلين) بنجاح!",
                "success_count": 1,
                "failure_count": 0
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="فشل إرسال الإشعار العام لكافة الأجهزة."
            )
            
    tokens = []
    
    if data.target == "students":
        # Fetch all student tokens
        students = db.query(Student).filter(Student.fcm_token != None, Student.fcm_token != "").all()
        tokens = [s.fcm_token for s in students]
        
    elif data.target == "institutes":
        # Fetch all institute admin tokens
        admins = db.query(InstituteAdmin).filter(InstituteAdmin.fcm_token != None, InstituteAdmin.fcm_token != "").all()
        tokens = [a.fcm_token for a in admins]
        
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="الجهة المستهدفة غير صحيحة! يجب أن تكون students أو institutes أو all"
        )
        
    if not tokens:
        return {
            "status": "success",
            "message": "لم يتم إرسال الإشعار لعدم وجود أجهزة مسجلة حالياً.",
            "success_count": 0,
            "failure_count": 0
        }
        
    res = send_broadcast_notification(tokens, data.title, data.body)
    return {
        "status": "success",
        "message": "تم إرسال الإشعار الجماعي بنجاح!",
        "success_count": res.get("success_count", 0),
        "failure_count": res.get("failure_count", 0)
    }
