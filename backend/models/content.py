from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

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
    id: str
    title: str
    description: str
    difficulty: DifficultyLevel
    content_type: ContentType
    duration: int  # in minutes
    modules: List[str]
    prerequisites: List[str] = []

class TrainingContent(BaseModel):
    id: str
    course_id: str
    title: str
    content: str
    content_type: ContentType
    order: int
    duration: int  # in minutes