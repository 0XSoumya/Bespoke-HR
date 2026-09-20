from unittest.mock import patch
from app.models.schemas.question_record import QuestionRecord
from app.models.schemas.followup_decision import FollowupDecision
from app.services.interview.followup_service import FollowupService


def test_followup_service_with_mock():
    record = QuestionRecord(
        question_id="q1",
        topic="RAG",
        difficulty="intermediate",
        main_question="Explain the key components of a RAG pipeline.",
        expected_concepts=["retriever", "generator", "context augmentation"],
        evaluation_criteria=["conceptual accuracy", "completeness"],
        main_answer="RAG uses a retriever and generator.",
    )

    with patch.object(
        FollowupService,
        "generate_followup",
        return_value=FollowupDecision(
            generate_followup=True,
            followup_question="What about context augmentation?",
            reason="Missing concept: context augmentation",
        ),
    ):
        service = FollowupService()
        decision = service.generate_followup(record)
        assert decision.generate_followup is True
        assert decision.followup_question == "What about context augmentation?"


if __name__ == "__main__":
    record = QuestionRecord(
        question_id="q1",
        topic="RAG",
        difficulty="intermediate",
        main_question="Explain the key components of a RAG pipeline.",
        expected_concepts=["retriever", "generator", "context augmentation"],
        evaluation_criteria=["conceptual accuracy", "completeness"],
        main_answer="RAG uses a retriever and generator.",
    )
    decision = FollowupService().generate_followup(record)
    print(decision.model_dump_json(indent=2))