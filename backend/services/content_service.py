from models.content import Course, TrainingContent, DifficultyLevel, ContentType
from models.user import User
from datetime import datetime
from bson import ObjectId
import json

class ContentService:
    def __init__(self, db):
        self.db = db
        self.courses_collection = db["courses"]
        self.content_collection = db["training_content"]
        self.users_collection = db["users"]
        self.chat_sessions_collection = db["chat_sessions"]
    
    async def initialize_sample_data(self):
        """Initialize sample courses and training content"""
        print("Initializing sample data...")
        
        # Clear existing data
        await self.courses_collection.delete_many({})
        await self.content_collection.delete_many({})
        
        # Sample courses
        sample_courses = [
            {
                "_id": ObjectId(),
                "title": "Phishing Awareness Basics",
                "description": "Learn the fundamentals of identifying phishing attempts",
                "difficulty": DifficultyLevel.BEGINNER,
                "content_type": ContentType.INTERACTIVE,
                "duration": 30,
                "modules": ["module1", "module2"],
                "prerequisites": []
            },
            {
                "_id": ObjectId(),
                "title": "Advanced Phishing Techniques",
                "description": "Learn about sophisticated phishing methods",
                "difficulty": DifficultyLevel.INTERMEDIATE,
                "content_type": ContentType.VIDEO,
                "duration": 45,
                "modules": ["module3", "module4", "module5"],
                "prerequisites": ["Phishing Awareness Basics"]
            },
            {
                "_id": ObjectId(),
                "title": "Phishing Incident Response",
                "description": "Learn how to respond to phishing incidents",
                "difficulty": DifficultyLevel.ADVANCED,
                "content_type": ContentType.SCENARIO,
                "duration": 60,
                "modules": ["module6", "module7", "module8", "module9"],
                "prerequisites": ["Advanced Phishing Techniques"]
            }
        ]
        
        # Insert courses
        await self.courses_collection.insert_many(sample_courses)
        
        # Sample training content
        sample_content = [
            # Beginner course content
            {
                "_id": ObjectId(),
                "course_id": sample_courses[0]["_id"],
                "title": "What is Phishing?",
                "content": """# What is Phishing?
                
Phishing is a type of cyber attack where attackers impersonate legitimate organizations to steal sensitive information such as:
- Usernames and passwords
- Credit card numbers
- Personal identification information

## Common Characteristics:
- Urgent or threatening language
- Requests for personal information
- Suspicious links or attachments
- Spelling and grammar errors""",
                "content_type": ContentType.INTERACTIVE,
                "order": 1,
                "duration": 10
            },
            {
                "_id": ObjectId(),
                "course_id": sample_courses[0]["_id"],
                "title": "Identifying Phishing Emails",
                "content": """# Identifying Phishing Emails
                
## Red Flags to Watch For:
1. **Generic greetings** like "Dear Customer" instead of your name
2. **Urgent requests** for immediate action
3. **Suspicious sender addresses** that don't match the organization
4. **Poor spelling and grammar**
5. **Requests for personal information**

## Example:
A legitimate bank will never ask you to verify your account by email.""",
                "content_type": ContentType.INTERACTIVE,
                "order": 2,
                "duration": 20
            },
            
            # Intermediate course content
            {
                "_id": ObjectId(),
                "course_id": sample_courses[1]["_id"],
                "title": "Spear Phishing",
                "content": """# Spear Phishing
                
Spear phishing targets specific individuals or organizations with personalized messages.

## Characteristics:
- Uses your name, position, or other personal details
- Appears to come from someone you know
- Often targets financial or HR departments

## Protection:
- Verify unusual requests via another channel
- Be cautious of emails requesting money transfers
- Use multi-factor authentication""",
                "content_type": ContentType.VIDEO,
                "order": 1,
                "duration": 15
            }
        ]
        
        # Insert content
        await self.content_collection.insert_many(sample_content)
        
        print("✅ Sample data initialized successfully")
    
    async def get_courses_by_level(self, level: str):
        """Get courses by difficulty level"""
        courses = await self.courses_collection.find({"difficulty": level}).to_list(length=None)
        return [self._format_course(course) for course in courses]
    
    async def get_course_content(self, course_id: str):
        """Get content for a specific course"""
        try:
            content = await self.content_collection.find(
                {"course_id": ObjectId(course_id)}
            ).sort("order", 1).to_list(length=None)
            return [self._format_content(item) for item in content]
        except:
            return []
    
    async def mark_course_complete(self, user_id: str, course_id: str):
        """Mark a course as complete for a user"""
        await self.users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$addToSet": {"completed_courses": course_id},
                "$set": {"updated_at": datetime.now()}
            }
        )
    
    async def get_user_progress(self, user_id: str):
        """Get user's learning progress"""
        user = await self.users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {}
        
        total_courses = await self.courses_collection.count_documents({})
        completed_count = len(user.get("completed_courses", []))
        
        return {
            "completed_courses": completed_count,
            "total_courses": total_courses,
            "progress_percentage": (completed_count / total_courses * 100) if total_courses > 0 else 0
        }
    
    async def get_user_by_id(self, user_id: str):
        """Get user by ID"""
        user = await self.users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return User(
                id=str(user["_id"]),
                name=user["name"],
                email=user["email"],
                classification=user["classification"],
                exam_score=user.get("exam_score"),
                completed_courses=user.get("completed_courses", []),
                current_course=user.get("current_course")
            )
        return None
    
    async def get_user_content(self, user_id: str):
        """Get user's training content"""
        user = await self.users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return []
        
        # This would normally fetch actual content from database
        # For now, return mock data based on user's classification
        level = user.get("classification", "beginner")
        
        if level == "beginner":
            return [
                TrainingContent(
                    id="1", course_id="1", title="Phishing Basics", 
                    content="Introduction to phishing", content_type=ContentType.INTERACTIVE,
                    order=1, duration=10
                )
            ]
        elif level == "intermediate":
            return [
                TrainingContent(
                    id="2", course_id="2", title="Advanced Techniques", 
                    content="Advanced phishing methods", content_type=ContentType.VIDEO,
                    order=1, duration=15
                )
            ]
        else:
            return [
                TrainingContent(
                    id="3", course_id="3", title="Incident Response", 
                    content="How to respond to phishing", content_type=ContentType.SCENARIO,
                    order=1, duration=20
                )
            ]
    
    async def save_chat_message(self, user_id: str, user_message: str, bot_response: str):
        """Save chat message to history"""
        message = {
            "sender": "user",
            "message": user_message,
            "timestamp": datetime.now()
        }
        
        response = {
            "sender": "bot",
            "message": bot_response,
            "timestamp": datetime.now()
        }
        
        await self.chat_sessions_collection.update_one(
            {"user_id": ObjectId(user_id)},
            {
                "$push": {
                    "messages": {
                        "$each": [message, response]
                    }
                },
                "$setOnInsert": {
                    "created_at": datetime.now()
                },
                "$set": {
                    "updated_at": datetime.now()
                }
            },
            upsert=True
        )
    
    async def get_chat_history(self, user_id: str):
        """Get user's chat history"""
        session = await self.chat_sessions_collection.find_one(
            {"user_id": ObjectId(user_id)}
        )
        
        if session and "messages" in session:
            return session["messages"]
        return []
    
    def _format_course(self, course):
        """Format course document for response"""
        return {
            "id": str(course["_id"]),
            "title": course["title"],
            "description": course["description"],
            "difficulty": course["difficulty"],
            "content_type": course["content_type"],
            "duration": course["duration"],
            "modules": course.get("modules", []),
            "prerequisites": course.get("prerequisites", [])
        }
    
    def _format_content(self, content):
        """Format content document for response"""
        return {
            "id": str(content["_id"]),
            "course_id": str(content["course_id"]),
            "title": content["title"],
            "content": content["content"],
            "content_type": content["content_type"],
            "order": content["order"],
            "duration": content["duration"]
        }