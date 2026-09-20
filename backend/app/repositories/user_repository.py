import uuid
from datetime import datetime, timezone
from typing import Any, Optional
from bson import ObjectId

from app.core.database import db


class UserRepository:
    COLLECTION_NAME = "users"

    @property
    def collection(self):
        return db[self.COLLECTION_NAME]

    async def ensure_indexes(self) -> None:
        """Create unique index on email."""
        await self.collection.create_index("email", unique=True)

    async def create_user(
        self,
        email: str,
        password_hash: str,
        full_name: str,
        role: str,
    ) -> dict[str, Any]:
        user_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        doc = {
            "_id": user_id,
            "email": email.lower().strip(),
            "password_hash": password_hash,
            "full_name": full_name.strip(),
            "role": role,
            "created_at": now,
            "updated_at": now,
        }
        await self.collection.insert_one(doc)
        return doc

    async def get_by_email(self, email: str) -> Optional[dict[str, Any]]:
        return await self.collection.find_one({"email": email.lower().strip()})

    async def get_by_id(self, user_id: str) -> Optional[dict[str, Any]]:
        # Check both string UUID and ObjectId
        doc = await self.collection.find_one({"_id": user_id})
        if not doc and ObjectId.is_valid(user_id):
            doc = await self.collection.find_one({"_id": ObjectId(user_id)})
        return doc

    async def list_candidates(self, limit: int = 100) -> list[dict[str, Any]]:
        cursor = self.collection.find(
            {"role": "candidate"},
            {"password_hash": 0},
        ).sort("created_at", -1).limit(limit)
        return [doc async for doc in cursor]

    async def delete_user(self, user_id: str) -> bool:
        res = await self.collection.delete_one({"_id": user_id})
        return res.deleted_count > 0
