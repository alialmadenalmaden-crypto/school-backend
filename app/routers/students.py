from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.tables import Student
from pydantic import BaseModel

router = APIRouter()

class SendAlertRequest(BaseModel):
    title: str
    message: str

@router.get("/")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).order_by(Student.created_at.desc()).all()
    
    return [
        {
            "id": str(student.id),
            "full_name": student.full_name,
            "email": student.email,
            "phone": student.phone,
            "is_email_verified": student.is_email_verified,
            "is_active": student.is_active,
            "created_at": student.created_at.isoformat() if student.created_at else ""
        }
        for student in students
    ]

@router.patch("/{student_id}/toggle-active/")
def toggle_student_active(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الطالب غير موجود!"
        )
    student.is_active = not student.is_active
    db.commit()
    return {
        "status": "success",
        "is_active": student.is_active
    }

@router.post("/{student_id}/send-alert/")
def send_student_alert(student_id: str, alert: SendAlertRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الطالب غير موجود!"
        )
    # Simulate sending push notification/SMS/email
    print(f"[SIMULATED ALERT] Sent to Student: {student.full_name} | Title: {alert.title} | Message: {alert.message}")
    return {
        "status": "success",
        "message": f"تم إرسال التنبيه إلى {student.full_name} بنجاح!"
    }


@router.delete("/{student_id}/")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الطالب غير موجود!"
        )
    try:
        db.delete(student)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل حذف الطالب من قاعدة البيانات: {str(e)}"
        )
    return {
        "status": "success",
        "message": "تم حذف حساب الطالب بنجاح!"
    }
