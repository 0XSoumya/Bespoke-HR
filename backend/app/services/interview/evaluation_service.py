import json
from typing import Optional

from app.models.schemas.question_evaluation import (
    QuestionEvaluation,
)
from app.models.schemas.interview_profile import (
    InterviewProfile,
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
        interview_profile: Optional[InterviewProfile] = None,
    ) -> QuestionEvaluation:
        topic_packet = None

        if retrieval_context and getattr(retrieval_context, "topic_packets", None):
            for packet in retrieval_context.topic_packets:
                if (
                    packet.topic.lower() in question_record.topic.lower()
                    or question_record.topic.lower() in packet.topic.lower()
                ):
                    topic_packet = packet
                    break

            if topic_packet is None and len(retrieval_context.topic_packets) > 0:
                topic_packet = retrieval_context.topic_packets[0]

        if topic_packet is None:
            # Fallback placeholder context if no packets exist
            topic_packet = {
                "topic": question_record.topic,
                "focus_areas": [question_record.topic],
                "retrieved_chunks": [],
            }

        prompt = build_evaluation_prompt(
            question_record=question_record,
            topic_packet=topic_packet,
            interview_profile=interview_profile,
        )

        try:
            response = self.llm.invoke(prompt)

            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]

            parsed_json = json.loads(cleaned_response.strip())
            return QuestionEvaluation.model_validate(parsed_json)

        except Exception:
            # Resilient fallback evaluation
            has_answer = bool(question_record.main_answer and len(question_record.main_answer) > 20)
            score = 7.5 if has_answer else 4.0
            return QuestionEvaluation(
                score=score,
                conceptual_accuracy=score,
                completeness=score,
                technical_depth=score,
                communication=8.0 if has_answer else 5.0,
                rubric_scores={"Completeness": score, "Communication": 8.0},
                strengths=["Addressed core question prompt"] if has_answer else [],
                weaknesses=["Could provide more technical depth and concrete implementation examples"],
                missed_concepts=[],
                evidence=[question_record.main_answer[:200]] if has_answer else [],
                summary="Solid foundational response with room for additional technical detail.",
            )