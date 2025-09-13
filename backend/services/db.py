from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
import os

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def init_db():
    """Initialize database connection"""
    try:
        db.client = AsyncIOMotorClient(settings.DATABASE_URL)
        # Extract database name from connection string or use default
        if "mongodb.net" in settings.DATABASE_URL:
            # MongoDB Atlas connection string
            db_name = settings.DATABASE_URL.split("/")[-1].split("?")[0]
        else:
            # Local MongoDB connection string
            db_name = "phishing_lms"
        
        db.db = db.client[db_name]
        
        # Test the connection
        await db.client.admin.command('ping')
        print(f"✅ MongoDB connection established successfully to database: {db_name}")
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise

async def get_database():
    """Get database instance"""
    if db.db is None:
        await init_db()
    return db.db

async def close_db():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("✅ MongoDB connection closed")

async def get_collection(collection_name: str):
    """Get a specific collection"""
    database = await get_database()
    return database[collection_name]