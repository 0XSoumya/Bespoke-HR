from pathlib import Path

from app.repositories.candidate_repository import (
    CandidateRepository,
)

from app.services.resume.resume_parser_service import (
    ResumeParserService,
)

from app.utils.pdf_loader import PDFLoader


class ResumeService:
    def __init__(self):
        self.parser = ResumeParserService()

        self.repository = CandidateRepository()

    async def process_resume_bytes(
        self,
        content: bytes,
        filename: str,
        target_role: str,
        user_id: str | None = None,
    ):
        resume_text = PDFLoader.load_pdf_from_bytes(
            content,
            file_name=filename,
        )

        profile = self.parser.parse_resume(
            resume_text
        )

        candidate_id = (
            await self.repository.create_candidate(
                target_role=target_role,
                resume_filename=filename,
                resume_text=resume_text,
                candidate_profile=profile.model_dump(),
                user_id=user_id,
            )
        )

        return {
            "candidate_id": candidate_id,
            "candidate_profile": profile,
        }

    async def process_resume(
        self,
        pdf_path: str,
        target_role: str,
        user_id: str | None = None,
    ):
        with open(pdf_path, "rb") as f:
            content = f.read()

        return await self.process_resume_bytes(
            content=content,
            filename=Path(pdf_path).name,
            target_role=target_role,
            user_id=user_id,
        )