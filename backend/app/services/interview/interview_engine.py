from typing import Optional

from app.models.schemas.interview_state import (
    InterviewState,
)
from app.models.schemas.interview_profile import (
    InterviewProfile,
)
from app.services.interview.interview_profile_service import (
    InterviewProfileService,
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
        self.profile_service = InterviewProfileService()
        self.interview_planner = InterviewPlannerService()
        self.query_planner = QueryPlannerService()
        self.retrieval_orchestrator = RetrievalOrchestrator()
        self.question_generator = QuestionGeneratorService()
        self.session_service = SessionService()

    def create_interview(
        self,
        candidate_id: str,
        role: str,
        candidate_profile,
        company: str = "Target Company",
        interview_stage: str = "Technical Round 1",
        interview_nature: str = "ML/AI Technical",
        number_of_questions: int = 3,
        number_of_followups: int = 1,
        job_description: Optional[str] = None,
        interview_profile: Optional[InterviewProfile] = None,
        interviewer_id: str | None = None,
        candidate_user_id: str | None = None,
        candidate_name: str | None = None,
        candidate_email: str | None = None,
        scheduled_at: str | None = None,
    ) -> InterviewState:
        # Build InterviewProfile if not provided
        if interview_profile is None:
            interview_profile = self.profile_service.build_interview_profile(
                candidate_profile=candidate_profile,
                company=company,
                target_role=role,
                interview_stage=interview_stage,
                interview_nature=interview_nature,
                number_of_questions=number_of_questions,
                number_of_followups=number_of_followups,
                job_description=job_description,
            )

        interview_plan = self.interview_planner.build_plan(
            target_role=role,
            candidate_profile=candidate_profile,
            num_questions=number_of_questions,
            interview_profile=interview_profile,
        )

        query_plan = self.query_planner.build_query_plan(
            role=role,
            interview_plan=interview_plan,
        )

        retrieval_context = self.retrieval_orchestrator.build_context(
            query_plan
        )

        question_set = self.question_generator.generate_questions(
            retrieval_context,
            num_questions=number_of_questions,
        )

        session = self.session_service.create_session(
            question_set
        )

        return InterviewState(
            candidate_id=candidate_id,
            role=role,
            company=company,
            interview_profile=interview_profile,
            candidate_profile=candidate_profile,
            retrieval_context=retrieval_context,
            question_set=question_set,
            session=session,
            status="interview_created",
            number_of_questions=number_of_questions,
            interviewer_id=interviewer_id,
            candidate_user_id=candidate_user_id,
            candidate_name=candidate_name,
            candidate_email=candidate_email,
            scheduled_at=scheduled_at,
        )