from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.user import User, UserCreate, UserResponse
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db):
        self.db = db
        self.users_collection = db["users"]
    
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password):
        return pwd_context.hash(password)
    
    async def get_user_by_email(self, email: str):
        return await self.users_collection.find_one({"email": email})
    
    async def create_user(self, user: UserCreate):
        hashed_password = self.get_password_hash(user.password)
        user_dict = {
            "name": user.name,
            "email": user.email,
            "password": hashed_password,
            "classification": "beginner",
            "exam_score": None,
            "completed_courses": [],
            "current_course": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        result = await self.users_collection.insert_one(user_dict)
        user_dict["id"] = str(result.inserted_id)
        return UserResponse(**user_dict)
    
    async def authenticate_user(self, email: str, password: str):
        user = await self.get_user_by_email(email)
        if not user:
            return False
        if not self.verify_password(password, user["password"]):
            return False
        
        return UserResponse(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            classification=user["classification"],
            exam_score=user.get("exam_score"),
            completed_courses=user.get("completed_courses", []),
            current_course=user.get("current_course")
        )
    
    async def create_access_token(self, user: UserResponse):
        to_encode = {
            "sub": user.id,
            "email": user.email,
            "name": user.name,
            "classification": user.classification
        }
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None