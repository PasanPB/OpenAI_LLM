from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.exam import ExamSubmission, ExamResult
from services.auth_service import verify_token
from services.exam_service import ExamService
from services.db import get_database

router = APIRouter()
security = HTTPBearer()

@router.get("/questions")
async def get_exam_questions():
    # This would return a set of phishing awareness questions
    # For now, returning mock data
    return [
        {
            "id": "1",
            "question": "Which of the following is a sign of a phishing email?",
            "options": [
                "Generic greeting like 'Dear Customer'",
                "Urgent request for personal information",
                "Suspicious email address",
                "All of the above"
            ],
            "correct_answer": 3
        },
        {
            "id": "2",
            "question": "What should you do if you receive a suspicious email?",
            "options": [
                "Click on links to verify",
                "Reply with your information",
                "Report it to your IT department",
                "Forward it to colleagues"
            ],
            "correct_answer": 2
        }
    ]

@router.post("/submit", response_model=ExamResult)
async def submit_exam(
    submission: ExamSubmission,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Verify user token
    payload = verify_token(credentials.credentials)
    user_id = payload.get("sub")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db = await get_database()
    exam_service = ExamService(db)
    
    # Calculate score and classify user
    result = await exam_service.evaluate_exam(submission, user_id)
    return result