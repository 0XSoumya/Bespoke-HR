from app.database.interview_repository import (
    InterviewRepository,
)

from app.database.candidate_repository import (
    CandidateRepository,
)

from app.models.schemas.interview_state import (
    InterviewState,
)


class InterviewPersistenceService:

    def __init__(self):

        self.interview_repository = (
            InterviewRepository()
        )

        self.candidate_repository = (
            CandidateRepository()
        )

    async def save_interview(
        self,
        state: InterviewState,
    ):

        existing = await (
            self.interview_repository
            .get(
                state.session
                .interview_id
            )
        )

        if existing is None:

            await (
                self.candidate_repository
                .create(
                    candidate_id=(
                        state.candidate_id
                    ),
                    profile=(
                        state
                        .candidate_profile
                    ),
                )
            )

            await (
                self.interview_repository
                .create(
                    state
                )
            )

        else:

            await (
                self.interview_repository
                .update(
                    state
                )
            )

    async def load_interview(
        self,
        interview_id: str,
    ):

        return await (
            self.interview_repository
            .get(
                interview_id
            )
        )

    async def delete_interview(
        self,
        interview_id: str,
    ):

        await (
            self.interview_repository
            .delete(
                interview_id
            )
        )