from app.graph.interview_graph import (
    build_interview_graph,
)

from app.models.schemas.interview_state import (
    InterviewState,
)

from app.services.interview.interview_engine import (
    InterviewEngine,
)

from app.services.interview.session_service import (
    SessionService,
)

from app.services.interview.interview_persistence_service import (
    InterviewPersistenceService,
)


class InterviewService:

    def __init__(self):

        self.engine = (
            InterviewEngine()
        )

        self.session_service = (
            SessionService()
        )

        self.persistence = (
            InterviewPersistenceService()
        )

        self.graph = (
            build_interview_graph()
        )

    async def create_interview(
        self,
        candidate_id: str,
        role: str,
        candidate_profile,
        company: str = "Target Company",
        interview_stage: str = "Technical Round 1",
        interview_nature: str = "ML/AI Technical",
        number_of_questions: int = 3,
        number_of_followups: int = 1,
        job_description: str | None = None,
        interview_profile=None,
        interviewer_id: str | None = None,
        candidate_user_id: str | None = None,
        candidate_name: str | None = None,
        candidate_email: str | None = None,
        scheduled_at: str | None = None,
    ) -> InterviewState:

        state = (
            self.engine
            .create_interview(
                candidate_id=candidate_id,
                role=role,
                candidate_profile=candidate_profile,
                company=company,
                interview_stage=interview_stage,
                interview_nature=interview_nature,
                number_of_questions=number_of_questions,
                number_of_followups=number_of_followups,
                job_description=job_description,
                interview_profile=interview_profile,
                interviewer_id=interviewer_id,
                candidate_user_id=candidate_user_id,
                candidate_name=candidate_name,
                candidate_email=candidate_email,
                scheduled_at=scheduled_at,
            )
        )

        current_question = (
            self.session_service
            .get_current_question(
                state.session
            )
        )

        state.current_question = (
            current_question
        )

        await (
            self.persistence
            .save_interview(
                state
            )
        )

        return state

    async def get_interview(
        self,
        interview_id: str,
    ):

        return await (
            self.persistence
            .load_interview(
                interview_id
            )
        )

    async def submit_answer(
        self,
        interview_id: str,
        answer: str,
    ):

        state = await (
            self.persistence
            .load_interview(
                interview_id
            )
        )

        if state is None:
            raise ValueError(
                "Interview not found"
            )

        if (
            getattr(
                state,
                "pending_followup",
                False
            )
        ):
            self.session_service.save_followup_answer(
                state.session,
                answer,
            )
        else:
            self.session_service.save_main_answer(
                state.session,
                answer,
            )

        # Sync the reference so graph nodes see the updated answer
        state.current_question = (
            self.session_service.get_current_question(
                state.session
            )
        )

        result = (
            self.graph.invoke(
                state
            )
        )

        print(
            "\nGRAPH RETURN TYPE:",
            type(result)
        )

        print(
            "\nGRAPH RESULT:"
        )

        print(result)

        if isinstance(
            result,
            dict,
        ):
            state = (
                InterviewState
                .model_validate(
                    result
                )
            )
        else:
            state = result
        
        state.current_question = (
            self.session_service.get_current_question(
                state.session
            )
        )

        await (
            self.persistence
            .save_interview(
                state
            )
        )

        return state

    async def get_current_question(
        self,
        interview_id: str,
    ):

        state = await (
            self.persistence
            .load_interview(
                interview_id
            )
        )

        if state is None:
            return None

        return (
            state.current_question
        )

    async def get_report(
        self,
        interview_id: str,
    ):

        state = await (
            self.persistence
            .load_interview(
                interview_id
            )
        )

        if state is None:
            return None

        return state.report

    async def get_raw_interview(self, interview_id: str):
        return await self.persistence.get_raw_document(interview_id)

    async def list_for_interviewer(self, interviewer_id: str, limit: int = 100):
        return await self.persistence.list_for_interviewer(interviewer_id, limit=limit)

    async def list_for_candidate(
        self,
        candidate_user_id: str | None = None,
        candidate_email: str | None = None,
        candidate_id: str | None = None,
        limit: int = 100,
    ):
        return await self.persistence.list_for_candidate(
            candidate_user_id=candidate_user_id,
            candidate_email=candidate_email,
            candidate_id=candidate_id,
            limit=limit,
        )

    async def list_all(self, limit: int = 100):
        return await self.persistence.list_all(limit=limit)

    async def get_analytics(self, interviewer_id: str | None = None):
        return await self.persistence.get_analytics(interviewer_id=interviewer_id)