from app.models.schemas.interview_state import (
    InterviewState,
)

from app.services.interview.interview_planner_service import (
    InterviewPlannerService,
)

from app.services.interview.query_planner_service import (
    QueryPlannerService,
)

from app.services.interview.retrieval_orchestrator import (
    RetrievalOrchestrator,
)

from app.services.interview.question_generator_service import (
    QuestionGeneratorService,
)

from app.services.interview.session_service import (
    SessionService,
)


class InterviewEngine:

    def __init__(self):

        self.interview_planner = (
            InterviewPlannerService()
        )

        self.query_planner = (
            QueryPlannerService()
        )

        self.retrieval_orchestrator = (
            RetrievalOrchestrator()
        )

        self.question_generator = (
            QuestionGeneratorService()
        )

        self.session_service = (
            SessionService()
        )

    def create_interview(
        self,
        candidate_id: str,
        role: str,
        candidate_profile,
        number_of_questions: int = 3,
        interviewer_id: str | None = None,
        candidate_user_id: str | None = None,
        candidate_name: str | None = None,
        candidate_email: str | None = None,
        scheduled_at: str | None = None,
    ) -> InterviewState:

        interview_plan = (
            self.interview_planner
            .build_plan(
                target_role=role,
                candidate_profile=(
                    candidate_profile
                ),
                num_questions=number_of_questions,
            )
        )

        query_plan = (
            self.query_planner
            .build_query_plan(
                role=role,
                interview_plan=(
                    interview_plan
                ),
            )
        )

        retrieval_context = (
            self.retrieval_orchestrator
            .build_context(
                query_plan
            )
        )

        question_set = (
            self.question_generator
            .generate_questions(
                retrieval_context,
                num_questions=number_of_questions,
            )
        )

        session = (
            self.session_service
            .create_session(
                question_set
            )
        )

        return InterviewState(
            candidate_id=(
                candidate_id
            ),
            role=role,
            candidate_profile=(
                candidate_profile
            ),
            retrieval_context=(
                retrieval_context
            ),
            question_set=(
                question_set
            ),
            session=session,
            status=(
                "interview_created"
            ),
            number_of_questions=number_of_questions,
            interviewer_id=interviewer_id,
            candidate_user_id=candidate_user_id,
            candidate_name=candidate_name,
            candidate_email=candidate_email,
            scheduled_at=scheduled_at,
        )