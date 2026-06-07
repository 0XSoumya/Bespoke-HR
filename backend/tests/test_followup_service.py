from app.models.schemas.question_record import (
    QuestionRecord,
)

from app.services.interview.followup_service import (
    FollowupService,
)


record = QuestionRecord(
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
        "RAG uses a retriever "
        "and generator."
    ),
)

decision = (
    FollowupService()
    .generate_followup(
        record
    )
)

print(
    decision.model_dump_json(
        indent=2
    )
)