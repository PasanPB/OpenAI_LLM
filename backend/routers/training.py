from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.auth_service import verify_token
from services.content_service import ContentService
from services.db import get_database

router = APIRouter()
security = HTTPBearer()

@router.get("/courses/{level}")
async def get_courses_by_level(
    level: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    verify_token(credentials.credentials)
    
    db = await get_database()
    content_service = ContentService(db)
    
    courses = await content_service.get_courses_by_level(level)
    return courses

@router.get("/content/{course_id}")
async def get_course_content(
    course_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    verify_token(credentials.credentials)
    
    db = await get_database()
    content_service = ContentService(db)
    
    content = await content_service.get_course_content(course_id)
    return content

@router.post("/complete/{course_id}")
async def mark_course_complete(
    course_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    payload = verify_token(credentials.credentials)
    user_id = payload.get("sub")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db = await get_database()
    content_service = ContentService(db)
    
    await content_service.mark_course_complete(user_id, course_id)
    return {"status": "success", "message": f"Course {course_id} marked as complete"}