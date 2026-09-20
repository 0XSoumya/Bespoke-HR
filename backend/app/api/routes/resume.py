from pathlib import Path
from typing import Any, Optional
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)

from app.api.deps import get_optional_user
from app.core.config.settings import settings
from app.services.resume.resume_service import ResumeService

router = APIRouter(
    prefix="/resume",
    tags=["resume"],
)

resume_service = ResumeService()


@router.post("/upload")
async def upload_resume(
    resume_file: UploadFile = File(...),
    target_role: str = Form(...),
    current_user: Optional[dict[str, Any]] = Depends(get_optional_user),
):
    if not resume_file.filename or not resume_file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF resume files (.pdf) are supported.",
        )

    # Sanitize filename (prevent path traversal or filesystem leakage)
    safe_filename = Path(resume_file.filename).name

    content = await resume_file.read()

    # Enforce file size limit
    if len(content) > settings.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Resume file size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)}MB.",
        )

    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format: file header is not a valid PDF.",
        )

    user_id = str(current_user["_id"]) if current_user else None

    try:
        result = await resume_service.process_resume_bytes(
            content=content,
            filename=safe_filename,
            target_role=target_role,
            user_id=user_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process resume. Please verify the document format.",
        )

    return {
        "candidate_id": result["candidate_id"],
        "candidate_profile": result["candidate_profile"].model_dump(),
    }