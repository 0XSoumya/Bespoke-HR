from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config.settings import settings

client = AsyncIOMotorClient(settings.MONGODB_URI)

db = client.ai_interview_system