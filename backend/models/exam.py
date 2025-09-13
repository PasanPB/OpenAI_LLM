from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ExamQuestion(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_answer: int
    explanation: str

class ExamSubmission(BaseModel):
    user_id: str
    answers: List[int]
    time_taken: int  # in seconds

class ExamResult(BaseModel):
    user_id: str
    score: float
    total_questions: int
    correct_answers: int
    classification: str
    submitted_at: datetime = datetime.now()