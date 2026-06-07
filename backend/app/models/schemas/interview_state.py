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


class InterviewState(
    BaseModel
):
    candidate_id: str

    role: str

    candidate_profile: (
        CandidateProfile
    )

    retrieval_context: (
        RetrievalContext | None
    ) = None

    question_set: (
        QuestionSet | None
    ) = None

    session: (
        InterviewSession | None
    ) = None

    current_question: (
        QuestionRecord | None
    ) = None

    current_answer: str | None = None

    followup_decision: (
        FollowupDecision | None
    ) = None

    pending_followup: bool = False

    report: (
        InterviewReport | None
    ) = None

    status: str = (
        "initialized"
    )