from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    password: str
    classification: str = "beginner"  # beginner, intermediate, advanced
    exam_score: Optional[float] = None
    completed_courses: List[str] = []
    current_course: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    classification: str
    exam_score: Optional[float] = None
    completed_courses: List[str] = []
    current_course: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str