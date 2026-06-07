from datetime import datetime

from app.core.database import db


class CandidateRepository:
    COLLECTION_NAME = "candidates"

    async def create_candidate(
        self,
        target_role: str,
        resume_filename: str,
        resume_text: str,
        candidate_profile: dict,
    ):
        document = {
            "target_role": target_role,
            "resume_filename": resume_filename,
            "resume_text": resume_text,
            "candidate_profile": candidate_profile,
            "created_at": datetime.utcnow(),
        }

        result = await db[
            self.COLLECTION_NAME
        ].insert_one(document)

        return str(result.inserted_id)

    async def get_candidate(
        self,
        candidate_id: str,
    ):
        from bson import ObjectId

        return await db[
            self.COLLECTION_NAME
        ].find_one(
            {
                "_id": ObjectId(candidate_id)
            }
        )