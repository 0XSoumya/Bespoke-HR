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

    async def list_for_interviewer(self, interviewer_id: str, limit: int = 100):
        return await self.interview_repository.list_for_interviewer(interviewer_id, limit=limit)

    async def list_for_candidate(
        self,
        candidate_user_id: str | None = None,
        candidate_email: str | None = None,
        candidate_id: str | None = None,
        limit: int = 100,
    ):
        return await self.interview_repository.list_for_candidate(
            candidate_user_id=candidate_user_id,
            candidate_email=candidate_email,
            candidate_id=candidate_id,
            limit=limit,
        )

    async def list_all(self, limit: int = 100):
        return await self.interview_repository.list_all(limit=limit)

    async def get_raw_document(self, interview_id: str):
        return await self.interview_repository.get_raw_document(interview_id)

    async def get_analytics(self, interviewer_id: str | None = None):
        return await self.interview_repository.get_analytics(interviewer_id=interviewer_id)