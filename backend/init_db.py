import asyncio
import os
import sys
from datetime import datetime, timedelta
from bson import ObjectId

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.db import init_db, get_database
from models.content import DifficultyLevel, ContentType

async def initialize_database():
    """Initialize the database with comprehensive sample data"""
    try:
        # Initialize database connection
        await init_db()
        db = await get_database()
        
        # Clear existing data
        await db.users.delete_many({})
        await db.courses.delete_many({})
        await db.training_content.delete_many({})
        await db.exam_results.delete_many({})
        await db.chat_sessions.delete_many({})
        
        print("✅ Cleared existing data")
        
        # Create indexes
        await db.users.create_index("email", unique=True)
        await db.courses.create_index("difficulty")
        await db.chat_sessions.create_index("user_id")
        await db.exam_results.create_index("user_id")
        
        print("✅ Database indexes created")
        
        # Insert sample data
        await insert_sample_data(db)
        
        print("✅ Sample data inserted successfully")
        print("✅ Database initialization completed successfully")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        # Close the database connection
        from services.db import close_db
        await close_db()

async def insert_sample_data(db):
    """Insert comprehensive sample data into all collections"""
    
    # Sample users
    sample_users = [
        {
            "_id": ObjectId(),
            "name": "John Doe",
            "email": "john.doe@company.com",
            "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # password: "secret"
            "classification": "beginner",
            "exam_score": 45.0,
            "completed_courses": [],
            "current_course": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "_id": ObjectId(),
            "name": "Jane Smith",
            "email": "jane.smith@company.com",
            "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # password: "secret"
            "classification": "intermediate",
            "exam_score": 75.0,
            "completed_courses": ["phishing-basics"],
            "current_course": "advanced-phishing",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "_id": ObjectId(),
            "name": "Mike Johnson",
            "email": "mike.johnson@company.com",
            "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # password: "secret"
            "classification": "advanced",
            "exam_score": 92.0,
            "completed_courses": ["phishing-basics", "advanced-phishing"],
            "current_course": "incident-response",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    ]
    
    # Sample courses
    sample_courses = [
        {
            "_id": "phishing-basics",
            "title": "Phishing Awareness Basics",
            "description": "Learn the fundamentals of identifying phishing attempts and protecting yourself online.",
            "difficulty": DifficultyLevel.BEGINNER,
            "content_type": ContentType.INTERACTIVE,
            "duration": 45,
            "modules": ["module-1", "module-2", "module-3"],
            "prerequisites": [],
            "created_at": datetime.now()
        },
        {
            "_id": "advanced-phishing",
            "title": "Advanced Phishing Techniques",
            "description": "Learn about sophisticated phishing methods and how to recognize them.",
            "difficulty": DifficultyLevel.INTERMEDIATE,
            "content_type": ContentType.VIDEO,
            "duration": 60,
            "modules": ["module-4", "module-5", "module-6"],
            "prerequisites": ["phishing-basics"],
            "created_at": datetime.now()
        },
        {
            "_id": "incident-response",
            "title": "Phishing Incident Response",
            "description": "Learn how to properly respond to phishing incidents and report them.",
            "difficulty": DifficultyLevel.ADVANCED,
            "content_type": ContentType.SCENARIO,
            "duration": 90,
            "modules": ["module-7", "module-8", "module-9"],
            "prerequisites": ["advanced-phishing"],
            "created_at": datetime.now()
        },
        {
            "_id": "social-engineering",
            "title": "Social Engineering Awareness",
            "description": "Understand social engineering tactics used in phishing attacks.",
            "difficulty": DifficultyLevel.INTERMEDIATE,
            "content_type": ContentType.INTERACTIVE,
            "duration": 50,
            "modules": ["module-10", "module-11"],
            "prerequisites": ["phishing-basics"],
            "created_at": datetime.now()
        }
    ]
    
    # Sample training content
    sample_content = [
        # Beginner course content
        {
            "_id": "module-1",
            "course_id": "phishing-basics",
            "title": "What is Phishing?",
            "content": """# Understanding Phishing

## What is Phishing?
Phishing is a type of cyber attack where attackers impersonate legitimate organizations to steal sensitive information such as:
- Usernames and passwords
- Credit card numbers
- Personal identification information
- Company confidential data

## Common Characteristics:
- Urgent or threatening language
- Requests for personal information
- Suspicious links or attachments
- Spelling and grammar errors
- Generic greetings instead of your name""",
            "content_type": ContentType.INTERACTIVE,
            "order": 1,
            "duration": 15,
            "created_at": datetime.now()
        },
        {
            "_id": "module-2",
            "course_id": "phishing-basics",
            "title": "Identifying Phishing Emails",
            "content": """# Identifying Phishing Emails

## Red Flags to Watch For:
1. **Generic greetings** like "Dear Customer" instead of your name
2. **Urgent requests** for immediate action
3. **Suspicious sender addresses** that don't match the organization
4. **Poor spelling and grammar**
5. **Requests for personal information**
6. **Suspicious links** (hover to see actual URL)
7. **Unexpected attachments**

## Example:
A legitimate bank will never ask you to verify your account by email. Always contact the organization directly through official channels.""",
            "content_type": ContentType.INTERACTIVE,
            "order": 2,
            "duration": 20,
            "created_at": datetime.now()
        },
        {
            "_id": "module-3",
            "course_id": "phishing-basics",
            "title": "Basic Protection Measures",
            "content": """# Basic Protection Measures

## How to Protect Yourself:
- **Verify sender addresses** carefully
- **Don't click suspicious links** - hover to see actual URL first
- **Use multi-factor authentication** whenever possible
- **Keep software updated** - browsers and security software
- **Report suspicious emails** to your IT department

## Best Practices:
- When in doubt, don't click!
- Contact the organization through official channels
- Use password managers to avoid entering credentials on phishing sites
- Regularly review account statements for suspicious activity""",
            "content_type": ContentType.QUIZ,
            "order": 3,
            "duration": 10,
            "created_at": datetime.now()
        },
        
        # Intermediate course content
        {
            "_id": "module-4",
            "course_id": "advanced-phishing",
            "title": "Spear Phishing Attacks",
            "content": """# Spear Phishing Attacks

## What is Spear Phishing?
Targeted phishing attacks against specific individuals or organizations using personalized information.

## Characteristics:
- Uses your name, position, or other personal details
- Appears to come from someone you know or trust
- Often targets financial, HR, or executive departments
- May reference recent events or projects

## Real-World Example:
An attacker researches a company's executives and sends a fake invoice request from the CEO to the finance department.""",
            "content_type": ContentType.VIDEO,
            "order": 1,
            "duration": 20,
            "created_at": datetime.now()
        },
        {
            "_id": "module-5",
            "course_id": "advanced-phishing",
            "title": "Business Email Compromise (BEC)",
            "content": """# Business Email Compromise (BEC)

## What is BEC?
Sophisticated attacks targeting businesses to initiate unauthorized wire transfers or obtain sensitive data.

## Common Scenarios:
- Fake executive requests for urgent wire transfers
- Compromised vendor requests with changed payment details
- Fake legal subpoenas or regulatory requests
- HR-related phishing for employee information

## Protection Strategies:
- Implement payment verification processes
- Train employees to recognize BEC patterns
- Use email authentication technologies (DMARC, DKIM, SPF)
- Establish clear procedures for financial transactions""",
            "content_type": ContentType.SCENARIO,
            "order": 2,
            "duration": 25,
            "created_at": datetime.now()
        },
        {
            "_id": "module-6",
            "course_id": "advanced-phishing",
            "title": "Advanced Detection Techniques",
            "content": """# Advanced Detection Techniques

## Technical Indicators:
- **Email header analysis** for spoofing detection
- **Domain age** and registration details
- **SSL certificate** validity and issuer
- **URL structure** and redirect patterns

## Behavioral Indicators:
- Unusual sending patterns or times
- Requests that bypass normal procedures
- Urgency that prevents verification
- Changes to established communication patterns""",
            "content_type": ContentType.INTERACTIVE,
            "order": 3,
            "duration": 15,
            "created_at": datetime.now()
        }
    ]
    
    # Sample exam results
    sample_exam_results = [
        {
            "_id": ObjectId(),
            "user_id": sample_users[0]["_id"],
            "score": 45.0,
            "total_questions": 10,
            "correct_answers": 4.5,
            "classification": "beginner",
            "submitted_at": datetime.now() - timedelta(days=7),
            "answers": [0, 1, 2, 3, 0, 1, 2, 3, 0, 1],
            "time_taken": 1200  # seconds
        },
        {
            "_id": ObjectId(),
            "user_id": sample_users[1]["_id"],
            "score": 75.0,
            "total_questions": 10,
            "correct_answers": 7.5,
            "classification": "intermediate",
            "submitted_at": datetime.now() - timedelta(days=5),
            "answers": [3, 2, 1, 0, 3, 2, 1, 0, 3, 2],
            "time_taken": 900  # seconds
        },
        {
            "_id": ObjectId(),
            "user_id": sample_users[2]["_id"],
            "score": 92.0,
            "total_questions": 10,
            "correct_answers": 9.2,
            "classification": "advanced",
            "submitted_at": datetime.now() - timedelta(days=3),
            "answers": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            "time_taken": 600  # seconds
        }
    ]
    
    # Sample chat sessions
    sample_chat_sessions = [
        {
            "user_id": sample_users[0]["_id"],
            "messages": [
                {
                    "sender": "user",
                    "message": "What should I do if I receive a suspicious email?",
                    "timestamp": datetime.now() - timedelta(hours=2)
                },
                {
                    "sender": "bot",
                    "message": "If you receive a suspicious email, do not click any links or download attachments. Forward it to your IT department for analysis and then delete it from your inbox.",
                    "timestamp": datetime.now() - timedelta(hours=2, minutes=1)
                },
                {
                    "sender": "user",
                    "message": "How can I tell if an email is phishing?",
                    "timestamp": datetime.now() - timedelta(hours=1)
                },
                {
                    "sender": "bot",
                    "message": "Look for red flags like generic greetings, urgent requests for personal information, suspicious sender addresses, poor spelling/grammar, and links that don't match the supposed sender's website.",
                    "timestamp": datetime.now() - timedelta(hours=1, minutes=1)
                }
            ],
            "created_at": datetime.now() - timedelta(hours=2),
            "updated_at": datetime.now() - timedelta(hours=1)
        },
        {
            "user_id": sample_users[1]["_id"],
            "messages": [
                {
                    "sender": "user",
                    "message": "What's the difference between phishing and spear phishing?",
                    "timestamp": datetime.now() - timedelta(days=1)
                },
                {
                    "sender": "bot",
                    "message": "Phishing is a broad attack targeting many people with generic messages, while spear phishing is highly targeted against specific individuals or organizations using personalized information to appear legitimate.",
                    "timestamp": datetime.now() - timedelta(days=1, minutes=2)
                }
            ],
            "created_at": datetime.now() - timedelta(days=1),
            "updated_at": datetime.now() - timedelta(days=1)
        }
    ]
    
    # Insert all sample data
    print("Inserting sample users...")
    await db.users.insert_many(sample_users)
    
    print("Inserting sample courses...")
    await db.courses.insert_many(sample_courses)
    
    print("Inserting sample training content...")
    await db.training_content.insert_many(sample_content)
    
    print("Inserting sample exam results...")
    await db.exam_results.insert_many(sample_exam_results)
    
    print("Inserting sample chat sessions...")
    await db.chat_sessions.insert_many(sample_chat_sessions)
    
    print(f"✅ Inserted {len(sample_users)} users")
    print(f"✅ Inserted {len(sample_courses)} courses")
    print(f"✅ Inserted {len(sample_content)} training content items")
    print(f"✅ Inserted {len(sample_exam_results)} exam results")
    print(f"✅ Inserted {len(sample_chat_sessions)} chat sessions")

if __name__ == "__main__":
    asyncio.run(initialize_database())