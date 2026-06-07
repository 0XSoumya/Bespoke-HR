import asyncio

from app.services.resume.resume_service import (
    ResumeService,
)


async def main():
    service = ResumeService()

    result = await service.process_resume(
        pdf_path="sample_resume.pdf",
        target_role="GenAI Engineer",
    )

    print("\nCandidate ID:")
    print(
        result["candidate_id"]
    )

    print("\nCandidate Profile:")
    print(
        result[
            "candidate_profile"
        ].model_dump_json(
            indent=2
        )
    )


if __name__ == "__main__":
    asyncio.run(main())