import json

from app.models.schemas.followup_decision import (
    FollowupDecision,
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
    ) -> FollowupDecision:

        if (
            len(
                question_record.followups
            )
            >= 2
        ):
            return FollowupDecision(
                generate_followup=False,
                reason="max_followups_reached",
            )

        prompt = (
            build_followup_prompt(
                question_record
            )
        )

        response = self.llm.invoke(
            prompt
        )

        cleaned_response = (
            response.strip()
        )

        if cleaned_response.startswith(
            "```"
        ):
            cleaned_response = (
                cleaned_response.replace(
                    "```json",
                    ""
                )
            )

            cleaned_response = (
                cleaned_response.replace(
                    "```",
                    ""
                )
            )

        cleaned_response = (
            cleaned_response.strip()
        )

        parsed_json = json.loads(
            cleaned_response
        )

        return (
            FollowupDecision
            .model_validate(
                parsed_json
            )
        )