from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.tables import Language
from pydantic import BaseModel
from typing import List, Optional
import uuid

router = APIRouter()

# --- Pydantic Schemas ---
class LanguageBase(BaseModel):
    name: str
    code: str
    flag_path: Optional[str] = None
    is_active: Optional[bool] = True

class LanguageCreate(LanguageBase):
    pass

class LanguageResponse(LanguageBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

# --- Endpoints ---

@router.get("/", response_model=List[LanguageResponse])
def get_languages(db: Session = Depends(get_db)):
    """Fetch all languages"""
    languages = db.query(Language).all()
    return languages

@router.post("/", response_model=LanguageResponse)
def create_language(lang: LanguageCreate, db: Session = Depends(get_db)):
    """Add a new language"""
    # Check if code already exists
    existing_lang = db.query(Language).filter(Language.code == lang.code).first()
    if existing_lang:
        raise HTTPException(status_code=400, detail="Language code already exists")
    
    new_language = Language(
        name=lang.name,
        code=lang.code,
        flag_path=lang.flag_path,
        is_active=lang.is_active
    )
    db.add(new_language)
    db.commit()
    db.refresh(new_language)
    return new_language

class LanguageUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    flag_path: Optional[str] = None
    is_active: Optional[bool] = None

@router.put("/{language_id}", response_model=LanguageResponse)
def update_language(language_id: uuid.UUID, lang_update: LanguageUpdate, db: Session = Depends(get_db)):
    """Update language details"""
    language = db.query(Language).filter(Language.id == language_id).first()
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    
    if lang_update.name is not None:
        language.name = lang_update.name
    if lang_update.code is not None:
        language.code = lang_update.code
    if lang_update.flag_path is not None:
        language.flag_path = lang_update.flag_path
    if lang_update.is_active is not None:
        language.is_active = lang_update.is_active
        
    db.commit()
    db.refresh(language)
    return language

@router.delete("/{language_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_language(language_id: uuid.UUID, db: Session = Depends(get_db)):
    """Delete a language completely"""
    language = db.query(Language).filter(Language.id == language_id).first()
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    
    db.delete(language)
    db.commit()
    return {"message": "Language deleted successfully"}
