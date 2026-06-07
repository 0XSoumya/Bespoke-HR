import json
from collections import defaultdict

from app.models.schemas.interview_report import (
    InterviewReport,
)

from app.services.llm.groq_service import (
    GroqService,
)

from app.services.interview.report_prompt import (
    build_report_prompt,
)


class ReportService:
    def __init__(self):
        self.llm = GroqService()

    def generate_report(
        self,
        question_records,
    ) -> InterviewReport:

        evaluations = []

        topic_scores = defaultdict(
            list
        )

        for record in (
            question_records
        ):
            if (
                record.evaluation
                is None
            ):
                continue

            evaluation = (
                record.evaluation
            )

            evaluations.append(
                {
                    "topic": record.topic,
                    "evaluation": (
                        evaluation.model_dump()
                    ),
                }
            )

            topic_scores[
                record.topic
            ].append(
                evaluation.score
            )

        avg_topic_scores = {}

        for (
            topic,
            scores,
        ) in topic_scores.items():

            avg_topic_scores[
                topic
            ] = round(
                sum(scores)
                / len(scores),
                2,
            )

        payload = {
            "topic_scores":
                avg_topic_scores,
            "evaluations":
                evaluations,
        }

        prompt = (
            build_report_prompt(
                json.dumps(
                    payload,
                    indent=2,
                )
            )
        )

        response = (
            self.llm.invoke(
                prompt
            )
        )

        cleaned = (
            response.strip()
        )

        if cleaned.startswith(
            "```"
        ):
            cleaned = (
                cleaned.replace(
                    "```json",
                    "",
                )
            )

            cleaned = (
                cleaned.replace(
                    "```",
                    "",
                )
            )

        cleaned = (
            cleaned.strip()
        )

        parsed_json = json.loads(
            cleaned
        )

        return (
            InterviewReport
            .model_validate(
                parsed_json
            )
        )