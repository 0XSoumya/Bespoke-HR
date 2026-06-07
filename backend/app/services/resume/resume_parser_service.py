import json

from app.models.schemas.candidate_profile import (
    CandidateProfile,
)

from app.services.llm.groq_service import GroqService

from app.services.resume.resume_parser_prompt import (
    build_resume_parser_prompt,
)


class ResumeParserService:
    def __init__(self):
        self.llm = GroqService()

    def parse_resume(
        self,
        resume_text: str,
    ) -> CandidateProfile:

        prompt = build_resume_parser_prompt(
            resume_text
        )

        response = self.llm.invoke(prompt)

        print("\nRAW RESPONSE:\n")
        print(response)
        print("\n" + "=" * 80 + "\n")

        cleaned_response = response.strip()

        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response.replace(
                "```json",
                ""
            )

            cleaned_response = cleaned_response.replace(
                "```",
                ""
            )

        cleaned_response = cleaned_response.strip()

        try:
            parsed_json = json.loads(
                cleaned_response
            )

        except json.JSONDecodeError:
            raise ValueError(
                "Resume parser returned invalid JSON."
            )

        return CandidateProfile.model_validate(
            parsed_json
        )