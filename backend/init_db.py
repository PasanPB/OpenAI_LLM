import asyncio
import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.db import init_db, get_database
from services.content_service import ContentService

async def initialize_database():
    """Initialize the database with sample data"""
    try:
        # Initialize database connection
        await init_db()
        db = await get_database()
        
        # Create indexes
        await db.users.create_index("email", unique=True)
        await db.courses.create_index("difficulty")
        await db.chat_sessions.create_index("user_id")
        
        print("✅ Database indexes created")
        
        # Insert sample data
        content_service = ContentService(db)
        await content_service.initialize_sample_data()
        
        print("✅ Database initialization completed successfully")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        raise
    finally:
        # Close the database connection
        from services.db import close_db
        await close_db()

if __name__ == "__main__":
    asyncio.run(initialize_database())