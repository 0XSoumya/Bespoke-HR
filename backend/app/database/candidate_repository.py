from app.core.database import db

from app.models.schemas.candidate_profile import (
    CandidateProfile,
)


class CandidateRepository:

    def __init__(self):
        self.collection = (
            db.candidates
        )

    async def create(
        self,
        candidate_id: str,
        profile: CandidateProfile,
    ):

        document = {
            "_id": candidate_id,
            "profile": (
                profile.model_dump()
            ),
        }

        await (
            self.collection
            .insert_one(
                document
            )
        )

    async def get(
        self,
        candidate_id: str,
    ):

        document = await (
            self.collection
            .find_one(
                {
                    "_id":
                        candidate_id
                }
            )
        )

        if document is None:
            return None

        return (
            CandidateProfile
            .model_validate(
                document["profile"]
            )
        )

    async def update(
        self,
        candidate_id: str,
        profile: CandidateProfile,
    ):

        await (
            self.collection
            .update_one(
                {
                    "_id":
                        candidate_id
                },
                {
                    "$set": {
                        "profile": (
                            profile
                            .model_dump()
                        )
                    }
                },
            )
        )

    async def delete(
        self,
        candidate_id: str,
    ):

        await (
            self.collection
            .delete_one(
                {
                    "_id":
                        candidate_id
                }
            )
        )