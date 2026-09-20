import uuid
from datetime import datetime, timezone
from typing import Any, Optional
from bson import ObjectId

from app.core.database import db
from app.models.schemas.candidate_profile import CandidateProfile


class CandidateRepository:
    COLLECTION_NAME = "candidates"

    @property
    def collection(self):
        return db[self.COLLECTION_NAME]

    async def create_candidate(
        self,
        target_role: str,
        resume_filename: str,
        resume_text: str,
        candidate_profile: dict[str, Any],
        user_id: Optional[str] = None,
        candidate_name: Optional[str] = None,
    ) -> str:
        candidate_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        document = {
            "_id": candidate_id,
            "target_role": target_role,
            "resume_filename": resume_filename,
            "resume_text": resume_text,
            "candidate_profile": candidate_profile,
            "user_id": user_id,
            "candidate_name": candidate_name or candidate_profile.get("full_name") or candidate_profile.get("name"),
            "created_at": now,
            "updated_at": now,
        }
        await self.collection.insert_one(document)
        return candidate_id

    async def create(
        self,
        candidate_id: str,
        profile: CandidateProfile,
        user_id: Optional[str] = None,
    ):
        """Save or update candidate profile by ID."""
        now = datetime.now(timezone.utc)
        doc = await self.get_candidate(candidate_id)
        if doc is None:
            document = {
                "_id": candidate_id,
                "candidate_profile": profile.model_dump(),
                "user_id": user_id,
                "created_at": now,
                "updated_at": now,
            }
            await self.collection.insert_one(document)
        else:
            await self.collection.update_one(
                {"_id": doc["_id"]},
                {
                    "$set": {
                        "candidate_profile": profile.model_dump(),
                        "updated_at": now,
                    }
                },
            )

    async def get_candidate(
        self,
        candidate_id: str,
    ) -> Optional[dict[str, Any]]:
        doc = await self.collection.find_one({"_id": candidate_id})
        if not doc and ObjectId.is_valid(candidate_id):
            doc = await self.collection.find_one({"_id": ObjectId(candidate_id)})
        return doc

    async def get(
        self,
        candidate_id: str,
    ) -> Optional[CandidateProfile]:
        doc = await self.get_candidate(candidate_id)
        if doc is None:
            return None
        profile_data = doc.get("candidate_profile") or doc.get("profile")
        if not profile_data:
            return None
        return CandidateProfile.model_validate(profile_data)

    async def list_for_user(self, user_id: str) -> list[dict[str, Any]]:
        cursor = self.collection.find(
            {"user_id": user_id},
            {"resume_text": 0},
        ).sort("created_at", -1)
        return [doc async for doc in cursor]

    async def list_all(self, limit: int = 100) -> list[dict[str, Any]]:
        cursor = self.collection.find(
            {},
            {"resume_text": 0},
        ).sort("created_at", -1).limit(limit)
        return [doc async for doc in cursor]

    async def delete(self, candidate_id: str) -> bool:
        res = await self.collection.delete_one({"_id": candidate_id})
        if res.deleted_count == 0 and ObjectId.is_valid(candidate_id):
            res = await self.collection.delete_one({"_id": ObjectId(candidate_id)})
        return res.deleted_count > 0