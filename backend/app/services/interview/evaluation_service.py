import json

from app.models.schemas.question_evaluation import (
    QuestionEvaluation,
)

from app.services.llm.groq_service import (
    GroqService,
)

from app.services.interview.evaluation_prompt import (
    build_evaluation_prompt,
)


class EvaluationService:
    def __init__(self):
        self.llm = GroqService()

    def evaluate_question(
        self,
        question_record,
        retrieval_context,
    ) -> QuestionEvaluation:

        topic_packet = None

        for packet in (
            retrieval_context.topic_packets
        ):
            if (
                packet.topic
                == question_record.topic
            ):
                topic_packet = packet
                break

        if topic_packet is None:
            raise ValueError(
                f"No topic packet found for "
                f"{question_record.topic}"
            )

        prompt = (
            build_evaluation_prompt(
                question_record,
                topic_packet,
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

        return (
            QuestionEvaluation
            .model_validate(
                parsed_json
            )
        )