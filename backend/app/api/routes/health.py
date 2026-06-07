from fastapi import APIRouter
from app.core.database import db

router = APIRouter()


@router.get("/health")
async def health_check():
    await db.command("ping")
    return {"status": "healthy"}