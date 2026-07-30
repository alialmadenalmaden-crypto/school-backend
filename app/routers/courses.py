from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.tables import Course, Institute, Category, CourseProgram, Level, Curriculum, Language
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

class CourseCreate(BaseModel):
    institute_slug: str
    title: str
    description: Optional[str] = None
    instructor_name: Optional[str] = None
    price: float
    seats_available: Optional[int] = 30
    registration_deadline: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    class_time: Optional[str] = "08:00 - 10:00"
    category_name: Optional[str] = None
    
    # Advanced Phase 3/6 Fields
    program_id: Optional[str] = None
    level_id: Optional[str] = None
    curriculum_id: Optional[str] = None
    language_id: Optional[str] = None
    period: Optional[str] = "morning" # morning, evening

@router.get("/catalog-info/")
def get_catalog_info(db: Session = Depends(get_db)):
    programs = db.query(CourseProgram).filter(CourseProgram.status == "active").all()
    levels = db.query(Level).filter(Level.status == "active").all()
    languages = db.query(Language).filter(Language.is_active == True).all()
    curriculums = db.query(Curriculum).filter(Curriculum.status == "active").all()
    
    return {
        "programs": [{"id": str(p.id), "name": p.name_ar} for p in programs],
        "levels": [{"id": str(l.id), "name": l.name_ar} for l in levels],
        "languages": [{"id": str(lg.id), "name": lg.name} for lg in languages],
        "curriculums": [{"id": str(c.id), "name": c.name} for c in curriculums]
    }

@router.get("/{institute_slug}")
def get_courses_by_institute(
    institute_slug: str, 
    program_id: Optional[str] = None,
    level_id: Optional[str] = None,
    language_id: Optional[str] = None,
    period: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Fetch courses belonging to the institute slug
    query = db.query(Course).join(Institute).filter(
        Institute.slug == institute_slug
    )
    
    if program_id:
        query = query.filter(Course.program_id == program_id)
    if level_id:
        query = query.filter(Course.level_id == level_id)
    if language_id:
        query = query.filter(Course.language_id == language_id)
    if period:
        query = query.filter(Course.period == period)
        
    courses = query.order_by(Course.created_at.desc()).all()
    
    # Fallback to mock data if DB is empty
    if not courses:
        return [
            {
                "id": "c1",
                "title": "دبلوم لغة إنجليزية مكثف",
                "description": "دورة أساسيات اللغة الإنجليزية والقراءة والكتابة والمحادثة اليومية.",
                "instructor_name": "أ. محمد أحمد",
                "price": 60.0,
                "image": "https://images.unsplash.com/photo-1546410531-bb4caa6b424d",
                "is_published": True,
                "seats_available": 30,
                "registration_deadline": "2026-08-15",
                "start_date": "2026-09-01",
                "end_date": "2026-10-01",
                "class_time": "08:00 - 10:00",
                "period": "morning",
                "jeep_number": "777111222",
                "category_name": "اللغات",
                "program": None,
                "level": None,
                "language": None,
                "curriculum": None
            }
        ]
        
    return [
        {
            "id": str(course.id),
            "title": course.title,
            "description": course.description,
            "instructor_name": course.instructor_name or "",
            "price": float(course.price),
            "image": course.image_url or f"https://api.dicebear.com/7.x/shapes/svg?seed={course.title}",
            "is_published": course.is_published,
            "seats_available": course.seats_available or 30,
            "registration_deadline": course.registration_deadline or "",
            "start_date": course.start_date or "",
            "end_date": course.end_date or "",
            "class_time": course.class_time or "08:00 - 10:00",
            "time": course.class_time or "08:00 - 10:00",
            "jeep_number": course.institute.jeep_number or "",
            "category_name": course.category_name or "",
            
            # Catalog details
            "program": {
                "id": str(course.program.id),
                "name_ar": course.program.name_ar,
                "name_en": course.program.name_en
            } if course.program else None,
            "level": {
                "id": str(course.level.id),
                "name_ar": course.level.name_ar,
                "name_en": course.level.name_en
            } if course.level else None,
            "language": {
                "id": str(course.language.id),
                "name": course.language.name,
                "code": course.language.code
            } if course.language else None,
            "curriculum": {
                "id": str(course.curriculum.id),
                "name": course.curriculum.name,
                "edition": course.curriculum.edition
            } if course.curriculum else None
        }
        for course in courses
    ]

@router.post("/")
def create_course(course_data: CourseCreate, db: Session = Depends(get_db)):
    # 1. Look up the institute by slug
    inst = db.query(Institute).filter(Institute.slug == course_data.institute_slug).first()
    if not inst:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المعهد غير موجود!"
        )
        
    # 2. Look up the category
    chosen_category = course_data.category_name if course_data.category_name else (inst.category if inst.category else "الحاسوب")
    parent_category_name = chosen_category.split(" - ")[0]
    cat = db.query(Category).filter(Category.name_ar == parent_category_name).first()
    if not cat:
        cat = db.query(Category).first()
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="الرجاء تهيئة الأقسام في قاعدة البيانات أولاً!"
            )
            
    # 3. Create course record
    new_course = Course(
        institute_id=inst.id,
        category_id=cat.id,
        category_name=course_data.category_name or chosen_category,
        title=course_data.title,
        description=course_data.description,
        instructor_name=course_data.instructor_name,
        price=course_data.price,
        image_url=f"https://api.dicebear.com/7.x/shapes/svg?seed={course_data.title}",
        is_published=True,
        seats_available=course_data.seats_available,
        registration_deadline=course_data.registration_deadline,
        start_date=course_data.start_date,
        end_date=course_data.end_date,
        class_time=course_data.class_time,
        period=course_data.period or "morning",
        
        # Link Phase 3/6 Entities
        program_id=course_data.program_id,
        level_id=course_data.level_id,
        curriculum_id=course_data.curriculum_id,
        language_id=course_data.language_id
    )
    
    try:
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل إضافة الكورس في قاعدة البيانات: {str(e)}"
        )
        
    return {
        "id": str(new_course.id),
        "title": new_course.title,
        "description": new_course.description,
        "instructor_name": new_course.instructor_name,
        "price": float(new_course.price),
        "image": new_course.image_url,
        "is_published": new_course.is_published,
        "seats_available": new_course.seats_available,
        "registration_deadline": new_course.registration_deadline,
        "start_date": new_course.start_date,
        "end_date": new_course.end_date,
        "class_time": new_course.class_time,
        "time": new_course.class_time,
        "category_name": new_course.category_name or ""
    }

@router.patch("/{course_id}/toggle/")
def toggle_course_publish(course_id: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الكورس غير موجود!"
        )
        
    course.is_published = not course.is_published
    db.commit()
    return {
        "status": "success",
        "is_published": course.is_published
    }

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    instructor_name: Optional[str] = None
    price: Optional[float] = None
    seats_available: Optional[int] = None
    registration_deadline: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    class_time: Optional[str] = None
    category_name: Optional[str] = None
    
    # Advanced Phase 3/6 Fields
    program_id: Optional[str] = None
    level_id: Optional[str] = None
    curriculum_id: Optional[str] = None
    language_id: Optional[str] = None
    period: Optional[str] = None

@router.put("/{course_id}/")
def update_course(course_id: str, course_data: CourseUpdate, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الكورس غير موجود!"
        )
        
    if course_data.title is not None:
        course.title = course_data.title
    if course_data.description is not None:
        course.description = course_data.description
    if course_data.instructor_name is not None:
        course.instructor_name = course_data.instructor_name
    if course_data.price is not None:
        course.price = course_data.price
    if course_data.seats_available is not None:
        course.seats_available = course_data.seats_available
    if course_data.registration_deadline is not None:
        course.registration_deadline = course_data.registration_deadline
    if course_data.start_date is not None:
        course.start_date = course_data.start_date
    if course_data.end_date is not None:
        course.end_date = course_data.end_date
    if course_data.class_time is not None:
        course.class_time = course_data.class_time
    if course_data.period is not None:
        course.period = course_data.period
        
    # Link Phase 3/6 updates
    if course_data.program_id is not None:
        course.program_id = course_data.program_id
    if course_data.level_id is not None:
        course.level_id = course_data.level_id
    if course_data.curriculum_id is not None:
        course.curriculum_id = course_data.curriculum_id
    if course_data.language_id is not None:
        course.language_id = course_data.language_id
        
    if course_data.category_name is not None:
        course.category_name = course_data.category_name
        parent_category_name = course_data.category_name.split(" - ")[0]
        cat = db.query(Category).filter(Category.name_ar == parent_category_name).first()
        if cat:
            course.category_id = cat.id
        
    db.commit()
    db.refresh(course)
    
    return {
        "status": "success",
        "course": {
            "id": str(course.id),
            "title": course.title,
            "description": course.description,
            "instructor_name": course.instructor_name,
            "price": float(course.price),
            "seats_available": course.seats_available,
            "registration_deadline": course.registration_deadline,
            "start_date": course.start_date,
            "end_date": course.end_date,
            "class_time": course.class_time,
            "time": course.class_time,
            "category_name": course.category_name or ""
        }
    }

@router.delete("/{course_id}/")
def delete_course(course_id: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الكورس غير موجود!"
        )
        
    try:
        db.delete(course)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل حذف الكورس: {str(e)}"
        )
        
    return {
        "status": "success",
        "message": "تم حذف الكورس بنجاح!"
    }
