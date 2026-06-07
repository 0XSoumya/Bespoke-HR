from datetime import (
    datetime,
)

from app.core.database import db

from app.models.schemas.interview_state import (
    InterviewState,
)


class InterviewRepository:

    def __init__(self):
        self.collection = (
            db.interviews
        )

    async def create(
        self,
        state: InterviewState,
    ):

        document = {
            "_id": (
                state.session
                .interview_id
            ),
            "candidate_id": (
                state.candidate_id
            ),
            "role": (
                state.role
            ),
            "status": (
                state.status
            ),
            "state": (
                state
                .model_dump()
            ),
            "created_at": (
                datetime.utcnow()
            ),
            "updated_at": (
                datetime.utcnow()
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
        interview_id: str,
    ):

        document = await (
            self.collection
            .find_one(
                {
                    "_id":
                        interview_id
                }
            )
        )

        if document is None:
            return None

        return (
            InterviewState
            .model_validate(
                document["state"]
            )
        )

    async def update(
        self,
        state: InterviewState,
    ):

        await (
            self.collection
            .update_one(
                {
                    "_id": (
                        state.session
                        .interview_id
                    )
                },
                {
                    "$set": {
                        "state": (
                            state
                            .model_dump()
                        ),
                        "status": (
                            state.status
                        ),
                        "updated_at": (
                            datetime.utcnow()
                        ),
                    }
                },
            )
        )

    async def delete(
        self,
        interview_id: str,
    ):

        await (
            self.collection
            .delete_one(
                {
                    "_id":
                        interview_id
                }
            )
        )