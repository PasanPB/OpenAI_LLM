from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routers import auth, exam, classifier, training, chatbot
from services.db import init_db
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database connection
    await init_db()
    yield
    # Clean up resources
    pass

app = FastAPI(title="Phishing Awareness LMS", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(exam.router, prefix="/api/exam", tags=["exam"])
app.include_router(classifier.router, prefix="/api/classifier", tags=["classifier"])
app.include_router(training.router, prefix="/api/training", tags=["training"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["chatbot"])

@app.get("/")
async def root():
    return {"message": "Phishing Awareness LMS API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)