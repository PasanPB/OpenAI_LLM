from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.auth_service import verify_token
from services.openai_service import OpenAIService
from services.content_service import get_user_content
from models.user import User
from typing import Dict
import json

router = APIRouter()
security = HTTPBearer()
openai_service = OpenAIService()

@router.post("/message")
async def chat_message(
    request: Dict[str, str],
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        # Verify user token
        payload = verify_token(credentials.credentials)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Get user data (you would fetch this from your database)
        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user's training content
        user_content = await get_user_content(user_id)
        
        # Get AI response
        response = await openai_service.get_chat_response(
            request.get("message", ""), 
            user, 
            user_content
        )
        
        return {"response": response}
    
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_user_by_id(user_id: str):
    # This would typically query your database
    # For now, returning a mock user
    return User(
        id=user_id,
        name="John Doe",
        email="john@example.com",
        classification="intermediate"
    )