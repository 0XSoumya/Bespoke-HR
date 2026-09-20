from unittest.mock import patch
from app.models.schemas.question_record import QuestionRecord
from app.models.schemas.question_evaluation import QuestionEvaluation
from app.models.schemas.context_packet import (
    TopicContextPacket,
    RetrievalContext,
)
from app.services.interview.evaluation_service import EvaluationService


def test_evaluation_service_with_mock():
    question_record = QuestionRecord(
        question_id="q1",
        topic="RAG",
        difficulty="intermediate",
        main_question="Explain the key components of a RAG pipeline.",
        expected_concepts=["retriever", "generator", "context augmentation"],
        evaluation_criteria=["conceptual accuracy", "completeness"],
        main_answer="A RAG system uses a retriever and generator.",
    )

    retrieval_context = RetrievalContext(
        role="GenAI Engineer",
        topic_packets=[
            TopicContextPacket(
                topic="RAG",
                focus_areas=["retrieval", "generation"],
                question_objectives=["Assess architecture"],
            )
        ],
    )

    mock_eval = QuestionEvaluation(
        score=8.5,
        conceptual_accuracy=8.5,
        completeness=8.0,
        technical_depth=8.5,
        communication=9.0,
        strengths=["Clear explanation of retriever"],
        weaknesses=["Omitted context augmentation details"],
        summary="Solid fundamental answer",
    )

    with patch.object(EvaluationService, "evaluate_question", return_value=mock_eval):
        evaluator = EvaluationService()
        result = evaluator.evaluate_question(
            question_record=question_record,
            retrieval_context=retrieval_context,
        )
        assert result.score == 8.5
        assert len(result.strengths) == 1


if __name__ == "__main__":
    question_record = QuestionRecord(
        question_id="q1",
        topic="RAG",
        difficulty="intermediate",
        main_question="Explain the key components of a RAG pipeline.",
        expected_concepts=["retriever", "generator", "context augmentation"],
        evaluation_criteria=["conceptual accuracy", "completeness"],
        main_answer="A RAG system uses a retriever to fetch relevant information and passes it to the generator.",
    )
    retrieval_context = RetrievalContext(
        role="GenAI Engineer",
        topic_packets=[
            TopicContextPacket(
                topic="RAG",
                focus_areas=["retrieval", "generation"],
                question_objectives=["Assess architecture"],
            )
        ],
    )
    evaluation = EvaluationService().evaluate_question(
        question_record=question_record,
        retrieval_context=retrieval_context,
    )
    print(evaluation.model_dump_json(indent=2))