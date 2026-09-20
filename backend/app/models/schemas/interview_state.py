from typing import Optional
from pydantic import BaseModel

from app.models.schemas.candidate_profile import (
    CandidateProfile,
)
from app.models.schemas.context_packet import (
    RetrievalContext,
)
from app.models.schemas.question_set import (
    QuestionSet,
)
from app.models.schemas.interview_session import (
    InterviewSession,
)
from app.models.schemas.interview_report import (
    InterviewReport,
)
from app.models.schemas.question_record import (
    QuestionRecord,
)
from app.models.schemas.followup_decision import (
    FollowupDecision,
)
from app.models.schemas.interview_profile import (
    InterviewProfile,
)


class InterviewState(BaseModel):
    candidate_id: str

    role: str

    company: str = "Target Company"

    interview_profile: Optional[InterviewProfile] = None

    candidate_profile: CandidateProfile

    retrieval_context: RetrievalContext | None = None

    question_set: QuestionSet | None = None

    session: InterviewSession | None = None

    current_question: QuestionRecord | None = None

    current_answer: str | None = None

    followup_decision: FollowupDecision | None = None

    pending_followup: bool = False

    report: InterviewReport | None = None

    status: str = "initialized"

    number_of_questions: int = 3
    interviewer_id: str | None = None
    candidate_user_id: str | None = None
    candidate_email: str | None = None
    candidate_name: str | None = None
    scheduled_at: str | None = None