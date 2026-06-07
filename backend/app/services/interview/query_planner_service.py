import json

from app.models.schemas.query_plan import (
    QueryPlan,
)

from app.services.llm.groq_service import (
    GroqService,
)

from app.services.interview.query_planner_prompt import (
    build_query_planner_prompt,
)


class QueryPlannerService:
    def __init__(self):
        self.llm = GroqService()

    def build_query_plan(
        self,
        role: str,
        interview_plan,
    ) -> QueryPlan:

        prompt = (
            build_query_planner_prompt(
                role=role,
                interview_plan=interview_plan,
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
                    "",
                )
            )

            cleaned_response = (
                cleaned_response.replace(
                    "```",
                    "",
                )
            )

        cleaned_response = (
            cleaned_response.strip()
        )

        parsed_json = json.loads(
            cleaned_response
        )

        return QueryPlan.model_validate(
            parsed_json
        )