import os
import tempfile

from fastapi import (
    APIRouter,
    File,
    Form,
    UploadFile,
)

from app.services.resume.resume_service import (
    ResumeService,
)

router = APIRouter(
    prefix="/resume",
    tags=["resume"],
)

resume_service = ResumeService()


@router.post("/upload")
async def upload_resume(
    resume_file: UploadFile = File(...),
    target_role: str = Form(...),
):
    suffix = os.path.splitext(
        resume_file.filename
    )[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    ) as temp_file:

        content = await resume_file.read()

        temp_file.write(content)

        temp_path = temp_file.name

    result = (
        await resume_service.process_resume(
            pdf_path=temp_path,
            target_role=target_role,
        )
    )

    return {
        "candidate_id":
            result["candidate_id"],

        "candidate_profile":
            result[
                "candidate_profile"
            ].model_dump(),
    }