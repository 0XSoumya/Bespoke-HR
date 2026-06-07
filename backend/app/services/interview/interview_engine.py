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
    ) -> InterviewState:

        interview_plan = (
            self.interview_planner
            .build_plan(
                target_role=role,
                candidate_profile=(
                    candidate_profile
                ),
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
                retrieval_context
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
        )