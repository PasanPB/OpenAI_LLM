from pydantic import BaseModel
from datetime import datetime
from typing import List

class ChatMessage(BaseModel):
    sender: str  # "user" or "bot"
    message: str
    timestamp: datetime

class ChatSession(BaseModel):
    user_id: str
    messages: List[ChatMessage] = []
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()