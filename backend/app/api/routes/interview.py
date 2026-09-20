from typing import Any, Optional
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.api.deps import (
    get_current_user,
    get_optional_user,
    require_interviewer,
)
from app.models.schemas.candidate_profile import (
    CandidateProfile,
)
from app.models.schemas.interview_create_request import (
    CreateInterviewRequest,
)
from app.models.schemas.interview_requests import (
    SubmitAnswerRequest,
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

interview_service = InterviewService()
candidate_repository = CandidateRepository()


def _check_interview_access(
    raw_interview: dict[str, Any],
    user: Optional[dict[str, Any]],
    require_ownership_for_interviewer: bool = False,
):
    """
    Object-level authorization check:
    - If user is a candidate: must match candidate_user_id or candidate_email or candidate_id.
    - If user is an interviewer: must match interviewer_id (or unassigned/legacy).
    """
    if not user:
        # If unauthenticated, allow in development/demo mode
        return

    role = user.get("role")
    user_id = str(user.get("_id"))
    user_email = user.get("email", "").lower()

    if role == "candidate":
        cand_user_id = str(raw_interview.get("candidate_user_id") or "")
        cand_email = (raw_interview.get("candidate_email") or "").lower()
        cand_id = str(raw_interview.get("candidate_id") or "")

        if cand_user_id and cand_user_id == user_id:
            return
        if cand_email and cand_email == user_email:
            return
        if cand_id and cand_id == user_id:
            return
        # If not matched, deny
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: you are not authorized to view this interview.",
        )

    if role == "interviewer":
        owner_id = raw_interview.get("interviewer_id")
        # If interview is assigned to an interviewer and doesn't match
        if require_ownership_for_interviewer and owner_id and str(owner_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: you did not create this interview.",
            )


@router.post("/create")
async def create_interview(
    request: CreateInterviewRequest,
    current_user: Optional[dict[str, Any]] = Depends(get_optional_user),
):
    # If user is authenticated as candidate, candidate cannot create interviews
    if current_user and current_user.get("role") == "candidate":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Candidates are not permitted to create interviews.",
        )

    candidate = await candidate_repository.get_candidate(request.candidate_id)

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    profile_data = candidate.get("candidate_profile") or candidate.get("profile")
    profile = CandidateProfile.model_validate(profile_data)

    interviewer_id = str(current_user["_id"]) if current_user else None
    cand_user_id = request.candidate_user_id or candidate.get("user_id")
    cand_email = request.candidate_email or candidate.get("candidate_email")
    cand_name = request.candidate_name or candidate.get("candidate_name")

    state = await interview_service.create_interview(
        candidate_id=request.candidate_id,
        role=request.role,
        candidate_profile=profile,
        number_of_questions=request.number_of_questions,
        interviewer_id=interviewer_id,
        candidate_user_id=cand_user_id,
        candidate_name=cand_name,
        candidate_email=cand_email,
        scheduled_at=request.scheduled_at,
    )

    return {
        "interview_id": state.session.interview_id,
        "status": state.status,
        "number_of_questions": state.number_of_questions,
        "current_question": (
            state.current_question.main_question if state.current_question else None
        ),
    }


@router.get("")
@router.get("/")
async def list_interviews(
    current_user: Optional[dict[str, Any]] = Depends(get_optional_user),
):
    """List interviews scoped to the authenticated user's role."""
    if not current_user:
        return await interview_service.list_all()

    role = current_user.get("role")
    user_id = str(current_user["_id"])

    if role == "interviewer":
        return await interview_service.list_for_interviewer(user_id)
    else:
        return await interview_service.list_for_candidate(
            candidate_user_id=user_id,
            candidate_email=current_user.get("email"),
        )


@router.get("/analytics")
async def get_analytics(
    current_user: Optional[dict[str, Any]] = Depends(get_optional_user),
):
    interviewer_id = str(current_user["_id"]) if current_user and current_user.get("role") == "interviewer" else None
    return await interview_service.get_analytics(interviewer_id=interviewer_id)


@router.get("/candidates")
async def list_candidates(
    current_user: Optional[dict[str, Any]] = Depends(get_optional_user),
):
    if current_user and current_user.get("role") == "candidate":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Candidates cannot access candidate lists.",
        )
    return await candidate_repository.list_all()


@router.get("/candidates/{candidate_id}")
async def get_candidate(
    candidate_id: str,
    current_user: Optional[dict[str, Any]] = Depends(get_optional_user),
):
    candidate = await candidate_repository.get_candidate(candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    # Object-level check: candidate can only view their own candidate profile
    if current_user and current_user.get("role") == "candidate":
        if str(candidate.get("user_id") or "") != str(current_user["_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to candidate profile.",
            )

    return {
        "candidate_id": str(candidate["_id"]),
        "target_role": candidate.get("target_role"),
        "candidate_name": candidate.get("candidate_name"),
        "resume_filename": candidate.get("resume_filename"),
        "candidate_profile": candidate.get("candidate_profile"),
        "created_at": candidate.get("created_at"),
    }


@router.get("/{interview_id}")
async def get_interview(
    interview_id: str,
    current_user: Optional[dict[str, Any]] = Depends(get_optional_user),
):
    raw_doc = await interview_service.get_raw_interview(interview_id)
    if raw_doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found",
        )

    _check_interview_access(raw_doc, current_user)

    interview = await interview_service.get_interview(interview_id)
    if interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found",
        )

    return interview.model_dump()


@router.get("/{interview_id}/current-question")
async def get_current_question(
    interview_id: str,
    current_user: Optional[dict[str, Any]] = Depends(get_optional_user),
):
    raw_doc = await interview_service.get_raw_interview(interview_id)
    if raw_doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found",
        )

    _check_interview_access(raw_doc, current_user)

    question = await interview_service.get_current_question(interview_id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )

    return question.model_dump()


@router.post("/{interview_id}/answer")
async def submit_answer(
    interview_id: str,
    request: SubmitAnswerRequest,
    current_user: Optional[dict[str, Any]] = Depends(get_optional_user),
):
    raw_doc = await interview_service.get_raw_interview(interview_id)
    if raw_doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found",
        )

    _check_interview_access(raw_doc, current_user)

    state = await interview_service.submit_answer(
        interview_id=interview_id,
        answer=request.answer,
    )

    return {
        "status": state.status,
        "pending_followup": state.pending_followup,
        "current_question": (
            state.current_question.model_dump()
            if state.current_question
            else None
        ),
        "report_available": state.report is not None,
    }


@router.get("/{interview_id}/report")
async def get_report(
    interview_id: str,
    current_user: Optional[dict[str, Any]] = Depends(get_optional_user),
):
    raw_doc = await interview_service.get_raw_interview(interview_id)
    if raw_doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found",
        )

    _check_interview_access(raw_doc, current_user)

    report = await interview_service.get_report(interview_id)
    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found or not yet generated",
        )

    # Privacy / Authorization check:
    # If the requester is a candidate, NEVER expose the recruiter report!
    if current_user and current_user.get("role") == "candidate":
        return {
            "candidate_report": report.candidate_report.model_dump(),
        }

    return report.model_dump()