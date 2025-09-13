import os
import openai
from openai import AsyncOpenAI
from models.user import User
from models.content import TrainingContent
from typing import List
import json

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def get_chat_response(self, message: str, user: User, user_content: List[TrainingContent]) -> str:
        # Prepare user context for the AI
        user_context = f"""
        User Information:
        - Name: {user.name}
        - Email: {user.email}
        - Classification: {user.classification}
        - Completed Courses: {[content.title for content in user_content if content.completed]}
        - Current Course: {next((content.title for content in user_content if content.current), 'None')}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are a helpful phishing awareness assistant for a corporate Learning Management System. 
                        Provide tailored advice based on the user's knowledge level: {user.classification}. 
                        Be supportive and educational. Focus on phishing awareness, prevention, and best practices.
                        The user has completed these courses: {[content.title for content in user_content if content.completed]}.
                        Always respond in a professional but friendly tone."""
                    },
                    {
                        "role": "user",
                        "content": f"{user_context}\n\nUser question: {message}"
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return "I'm sorry, I'm having trouble connecting to the knowledge base. Please try again later."