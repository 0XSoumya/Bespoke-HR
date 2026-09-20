import json
import re
from typing import Optional

from app.models.schemas.followup_decision import (
    FollowupDecision,
)
from app.models.schemas.interview_profile import (
    InterviewProfile,
)
from app.services.llm.groq_service import (
    GroqService,
)
from app.services.interview.followup_prompt import (
    build_followup_prompt,
)


class FollowupService:
    def __init__(self):
        self.llm = GroqService()

    def generate_followup(
        self,
        question_record,
        max_followups: int = 1,
        interview_profile: Optional[InterviewProfile] = None,
    ) -> FollowupDecision:
        if max_followups <= 0 or len(question_record.followups) >= max_followups:
            return FollowupDecision(
                generate_followup=False,
                reason="max_followups_reached",
            )

        prompt = build_followup_prompt(
            question_record
        )

        try:
            response = self.llm.invoke(prompt)

            cleaned_response = response.strip()
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.replace("```json", "")
                cleaned_response = cleaned_response.replace("```", "")
            cleaned_response = cleaned_response.strip()

            json_match = re.search(
                r"\{[\s\S]*\}",
                cleaned_response,
            )

            if not json_match:
                return FollowupDecision(
                    generate_followup=False,
                    reason="parse_fallback",
                )

            parsed_json = json.loads(json_match.group())
            return FollowupDecision.model_validate(parsed_json)

        except Exception:
            return FollowupDecision(
                generate_followup=False,
                reason="error_fallback",
            )