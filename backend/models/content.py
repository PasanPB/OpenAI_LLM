from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ContentType(str, Enum):
    VIDEO = "video"
    INTERACTIVE = "interactive"
    SCENARIO = "scenario"
    QUIZ = "quiz"

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Course(BaseModel):
    id: str = Field(..., alias="_id")
    title: str
    description: str
    difficulty: DifficultyLevel
    content_type: ContentType
    duration: int
    modules: List[str]
    prerequisites: List[str] = []
    created_at: datetime = datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class TrainingContent(BaseModel):
    id: str = Field(..., alias="_id")
    course_id: str
    title: str
    content: str
    content_type: ContentType
    order: int
    duration: int
    created_at: datetime = datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}