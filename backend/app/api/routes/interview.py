from fastapi import (
    APIRouter,
    HTTPException,
)

from app.models.schemas.interview_requests import (
    SubmitAnswerRequest,
)

from app.models.schemas.interview_create_request import (
    CreateInterviewRequest,
)

from app.models.schemas.candidate_profile import (
    CandidateProfile,
)

from app.repositories.candidate_repository import (
    CandidateRepository,
)

from app.services.interview.interview_service import (
    InterviewService,
)

router = APIRouter(
    prefix="/interviews",
    tags=["interviews"],
)

interview_service = (
    InterviewService()
)

candidate_repository = (
    CandidateRepository()
)


@router.post(
    "/create"
)
async def create_interview(
    request: CreateInterviewRequest,
):

    candidate = await (
        candidate_repository
        .get_candidate(
            request.candidate_id
        )
    )

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Candidate not found"
            ),
        )

    profile = (
        CandidateProfile
        .model_validate(
            candidate[
                "candidate_profile"
            ]
        )
    )

    state = await (
        interview_service
        .create_interview(
            candidate_id=(
                request.candidate_id
            ),
            role=request.role,
            candidate_profile=profile,
        )
    )

    return {
        "interview_id":
            (
                state.session
                .interview_id
            ),
        "status":
            state.status,
        "current_question":
            (
                state.current_question
                .main_question
            ),
    }


@router.get(
    "/{interview_id}"
)
async def get_interview(
    interview_id: str,
):

    interview = await (
        interview_service
        .get_interview(
            interview_id
        )
    )

    if interview is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Interview not found"
            ),
        )

    return (
        interview
        .model_dump()
    )


@router.get(
    "/{interview_id}/current-question"
)
async def get_current_question(
    interview_id: str,
):

    question = await (
        interview_service
        .get_current_question(
            interview_id
        )
    )

    if question is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Question not found"
            ),
        )

    return (
        question
        .model_dump()
    )


@router.post(
    "/{interview_id}/answer"
)
async def submit_answer(
    interview_id: str,
    request: (
        SubmitAnswerRequest
    ),
):

    state = await (
        interview_service
        .submit_answer(
            interview_id=(
                interview_id
            ),
            answer=(
                request.answer
            ),
        )
    )

    return {
        "status":
            state.status,

        "pending_followup":
            state.pending_followup,

        "current_question":
            (
                state.current_question
                .model_dump()
                if state.current_question
                else None
            ),

        "report_available":
            (
                state.report
                is not None
            ),
    }


@router.get(
    "/{interview_id}/report"
)
async def get_report(
    interview_id: str,
):

    report = await (
        interview_service
        .get_report(
            interview_id
        )
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Report not found"
            ),
        )

    return (
        report
        .model_dump()
    )