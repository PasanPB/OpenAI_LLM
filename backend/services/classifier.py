class ClassifierService:
    def __init__(self, db):
        self.db = db
        self.users_collection = db["users"]
    
    def classify_user(self, score: float) -> str:
        if score < 50:
            return "beginner"
        elif score < 80:
            return "intermediate"
        else:
            return "advanced"
    
    async def update_user_classification(self, user_id: str, classification: str):
        await self.users_collection.update_one(
            {"_id": user_id},
            {"$set": {"classification": classification, "updated_at": datetime.now()}}
        )