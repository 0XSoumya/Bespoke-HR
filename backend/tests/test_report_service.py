from app.models.schemas.question_record import QuestionRecord
from app.services.interview.report_service import ReportService


def test_generate_report():
    records = [
        QuestionRecord(
            question_id="q1",
            topic="RAG",
            difficulty="intermediate",
            main_question="How does retrieval augmented generation work?",
            evaluation={
                "score": 8.8,
                "strengths": ["Strong RAG understanding"],
                "weaknesses": ["Missed context augmentation"],
            },
        ),
        QuestionRecord(
            question_id="q2",
            topic="Embeddings",
            difficulty="intermediate",
            main_question="Explain dense vs sparse embeddings.",
            evaluation={
                "score": 8.0,
                "strengths": ["Good embedding knowledge"],
                "weaknesses": ["Limited depth"],
            },
        ),
    ]

    report = ReportService().generate_report(records)
    assert report is not None
    assert report.candidate_report is not None
    assert report.candidate_report.overall_score > 0