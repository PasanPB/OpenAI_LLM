from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.auth_service import verify_token
from services.classifier_service import ClassifierService
from services.db import get_database

router = APIRouter()
security = HTTPBearer()

@router.post("/classify/{user_id}")
async def classify_user(
    user_id: str,
    score: float,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Verify admin token or same user
    verify_token(credentials.credentials)
    
    db = await get_database()
    classifier_service = ClassifierService(db)
    
    classification = classifier_service.classify_user(score)
    
    # Update user classification in database
    await classifier_service.update_user_classification(user_id, classification)
    
    return {"user_id": user_id, "classification": classification}