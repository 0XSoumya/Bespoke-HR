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

    async def process_resume(
        self,
        pdf_path: str,
        target_role: str,
    ):
        resume_text = PDFLoader.load_pdf(
            pdf_path
        )

        profile = self.parser.parse_resume(
            resume_text
        )

        candidate_id = (
            await self.repository.create_candidate(
                target_role=target_role,
                resume_filename=Path(
                    pdf_path
                ).name,
                resume_text=resume_text,
                candidate_profile=profile.model_dump(),
            )
        )

        return {
            "candidate_id": candidate_id,
            "candidate_profile": profile,
        }