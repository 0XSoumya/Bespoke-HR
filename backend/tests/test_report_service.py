from app.models.schemas.question_record import (
    QuestionRecord,
)

from app.services.interview.report_service import (
    ReportService,
)


records = [
    QuestionRecord(
        question_id="q1",
        topic="RAG",
        difficulty="intermediate",
        main_question="Question",
        evaluation={
            "score": 8.8,
            "strengths": [
                "Strong RAG understanding"
            ],
            "weaknesses": [
                "Missed context augmentation"
            ],
        },
    ),
    QuestionRecord(
        question_id="q2",
        topic="Embeddings",
        difficulty="intermediate",
        main_question="Question",
        evaluation={
            "score": 8.0,
            "strengths": [
                "Good embedding knowledge"
            ],
            "weaknesses": [
                "Limited depth"
            ],
        },
    ),
]

report = (
    ReportService()
    .generate_report(
        records
    )
)

print(
    report.model_dump_json(
        indent=2
    )
)