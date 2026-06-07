from app.models.schemas.question_record import (
    QuestionRecord,
)

from app.models.schemas.context_packet import (
    RetrievedChunk,
    TopicContextPacket,
    RetrievalContext,
)

from app.services.interview.evaluation_service import (
    EvaluationService,
)


question_record = QuestionRecord(
    question_id="q1",
    topic="RAG",
    difficulty="intermediate",

    main_question=(
        "Explain the key "
        "components of a "
        "RAG pipeline."
    ),

    expected_concepts=[
        "retriever",
        "generator",
        "context augmentation",
    ],

    evaluation_criteria=[
        "conceptual accuracy",
        "completeness",
    ],

    main_answer=(
        "A RAG system uses a retriever "
        "to fetch relevant information "
        "from a knowledge source and "
        "passes the retrieved content "
        "to the generator to create "
        "the final response."
    ),
)

retrieval_context = RetrievalContext(
    role="GenAI Engineer",

    topic_packets=[
        TopicContextPacket(
            topic="RAG",

            focus_areas=[
                "retrieval",
                "generation",
            ],

            question_objectives=[
                "assess conceptual understanding"
            ],

            retrieved_chunks=[
                RetrievedChunk(
                    chunk=(
                        "RAG combines a "
                        "retriever with a "
                        "generator and uses "
                        "retrieved context."
                    ),
                    metadata={},
                    retrieval_count=3,
                )
            ],
        )
    ],
)

evaluation = (
    EvaluationService()
    .evaluate_question(
        question_record,
        retrieval_context,
    )
)

print(
    evaluation.model_dump_json(
        indent=2
    )
)