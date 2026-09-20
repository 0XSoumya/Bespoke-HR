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
from app.services.interview.interview_profile_service import (
    InterviewProfileService,
)

router = APIRouter(
    prefix="/interviews",
    tags=["interviews"],
)

interview_service = InterviewService()
candidate_repository = CandidateRepository()
profile_service = InterviewProfileService()


def _check_interview_access(
    raw_interview: dict[str, Any],
    user: Optional[dict[str, Any]],
    require_ownership_for_interviewer: bool = False,
):
    """
    Object-level authorization check:
    - If interview is owned by a candidate, unauthenticated requests are denied.
    - If user is a candidate: must match candidate_user_id, candidate_email, or candidate_id.
    - If user is an interviewer: must match interviewer_id if assigned.
    """
    cand_user_id = str(raw_interview.get("candidate_user_id") or "")
    cand_email = (raw_interview.get("candidate_email") or "").lower().strip()
    cand_id = str(raw_interview.get("candidate_id") or "")

    if not user:
        if cand_user_id or cand_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required to access this interview session.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return

    role = user.get("role", "candidate")
    user_id = str(user.get("_id"))
    user_email = user.get("email", "").lower().strip()

    if role == "candidate":
        if cand_user_id and cand_user_id == user_id:
            return
        if cand_email and cand_email == user_email:
            return
        if cand_id and cand_id == user_id:
            return
        # If interview is not assigned to any user, permit the logged-in candidate
        if not cand_user_id and not cand_email:
            return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: you are not authorized to access this interview session.",
        )

    if role == "interviewer":
        owner_id = raw_interview.get("interviewer_id")
        if require_ownership_for_interviewer and owner_id and str(owner_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: you did not create this interview.",
            )


@router.post("/profile-preview")
async def preview_interview_profile(
    request: CreateInterviewRequest,
    current_user: Optional[dict[str, Any]] = Depends(get_optional_user),
):
    """
    Generates and previews the tailored Interview Profile (company intelligence,
    rubric criteria, and evidence sources) prior to starting the session.
    """
    candidate = await candidate_repository.get_candidate(request.candidate_id)
    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    profile_data = candidate.get("candidate_profile") or candidate.get("profile")
    profile = CandidateProfile.model_validate(profile_data)

    interview_profile = profile_service.build_interview_profile(
        candidate_profile=profile,
        company=request.company,
        target_role=request.role,
        interview_stage=request.interview_stage,
        interview_nature=request.interview_nature,
        number_of_questions=request.number_of_questions,
        number_of_followups=request.number_of_followups,
        job_description=request.job_description,
    )

    return interview_profile.model_dump()


@router.post("/create")
async def create_interview(
    request: CreateInterviewRequest,
    current_user: Optional[dict[str, Any]] = Depends(get_optional_user),
):
    """
    Creates a tailored preparation interview session centered on Candidate + Company + Stage + Nature.
    """
    candidate = await candidate_repository.get_candidate(request.candidate_id)
    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    profile_data = candidate.get("candidate_profile") or candidate.get("profile")
    profile = CandidateProfile.model_validate(profile_data)

    # Candidate ownership binding
    cand_user_id = (
        str(current_user["_id"])
        if current_user and current_user.get("role") == "candidate"
        else (request.candidate_user_id or candidate.get("user_id"))
    )
    cand_email = (
        current_user.get("email")
        if current_user and current_user.get("role") == "candidate"
        else (request.candidate_email or candidate.get("candidate_email"))
    )
    cand_name = (
        current_user.get("full_name")
        if current_user and current_user.get("role") == "candidate"
        else (request.candidate_name or candidate.get("candidate_name"))
    )
    interviewer_id = (
        str(current_user["_id"])
        if current_user and current_user.get("role") == "interviewer"
        else None
    )

    state = await interview_service.create_interview(
        candidate_id=request.candidate_id,
        role=request.role,
        candidate_profile=profile,
        company=request.company,
        interview_stage=request.interview_stage,
        interview_nature=request.interview_nature,
        number_of_questions=request.number_of_questions,
        number_of_followups=request.number_of_followups,
        job_description=request.job_description,
        interviewer_id=interviewer_id,
        candidate_user_id=cand_user_id,
        candidate_name=cand_name,
        candidate_email=cand_email,
        scheduled_at=request.scheduled_at,
    )

    return {
        "interview_id": state.session.interview_id,
        "status": state.status,
        "company": state.company,
        "role": state.role,
        "number_of_questions": state.number_of_questions,
        "interview_profile": (
            state.interview_profile.model_dump()
            if state.interview_profile
            else None
        ),
        "current_question": (
            state.current_question.model_dump()
            if state.current_question
            else None
        ),
    }


@router.get("")
@router.get("/")
async def list_interviews(
    current_user: Optional[dict[str, Any]] = Depends(get_optional_user),
):
    """List preparation interviews scoped to the authenticated candidate or interviewer."""
    if not current_user:
        return await interview_service.list_all(limit=20)

    role = current_user.get("role", "candidate")
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
    interviewer_id = (
        str(current_user["_id"])
        if current_user and current_user.get("role") == "interviewer"
        else None
    )
    return await interview_service.get_analytics(interviewer_id=interviewer_id)


@router.get("/candidates")
async def list_candidates(
    current_user: Optional[dict[str, Any]] = Depends(get_optional_user),
):
    if current_user and current_user.get("role") == "candidate":
        user_id = str(current_user["_id"])
        return await candidate_repository.list_for_user(user_id)
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

    if current_user and current_user.get("role") == "candidate":
        cand_uid = str(candidate.get("user_id") or "")
        if cand_uid and cand_uid != str(current_user["_id"]):
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

    raw_state = raw_doc.get("state", {})
    profile_data = raw_state.get("interview_profile")

    resp = {
        "interview_id": interview_id,
        "company": raw_doc.get("company") or (profile_data.get("company") if profile_data else "Target Company"),
        "role": raw_doc.get("role", ""),
        "interview_stage": raw_doc.get("interview_stage") or (profile_data.get("interview_stage") if profile_data else "Technical Round 1"),
        "interview_nature": raw_doc.get("interview_nature") or (profile_data.get("interview_nature") if profile_data else "ML/AI Technical"),
        "preparation_report": (
            report.preparation_report.model_dump()
            if report.preparation_report
            else None
        ),
        "candidate_report": (
            report.candidate_report.model_dump()
            if report.candidate_report
            else None
        ),
        "interview_profile": profile_data,
    }

    if not current_user or current_user.get("role") != "candidate":
        if report.recruiter_report:
            resp["recruiter_report"] = report.recruiter_report.model_dump()

    return resp