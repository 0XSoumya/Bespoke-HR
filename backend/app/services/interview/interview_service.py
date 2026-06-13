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
    ) -> InterviewState:

        state = (
            self.engine
            .create_interview(
                candidate_id=(
                    candidate_id
                ),
                role=role,
                candidate_profile=(
                    candidate_profile
                ),
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