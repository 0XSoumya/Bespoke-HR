from app.models.schemas.question_set import QuestionSet
from app.models.schemas.interview_question import InterviewQuestion
from app.services.interview.session_service import SessionService


def test_session_service_lifecycle():
    question_set = QuestionSet(
        role="GenAI Engineer",
        questions=[
            InterviewQuestion(
                question_id="q1",
                topic="RAG",
                difficulty="intermediate",
                question="Explain the key components of a RAG pipeline.",
            ),
            InterviewQuestion(
                question_id="q2",
                topic="Embeddings",
                difficulty="intermediate",
                question="What are embeddings?",
            ),
        ],
    )

    service = SessionService()
    session = service.create_session(question_set)

    assert session.interview_id is not None
    assert len(session.question_records) == 2

    current = service.get_current_question(session)
    assert current.main_question == "Explain the key components of a RAG pipeline."

    service.save_main_answer(session, "A RAG pipeline retrieves relevant documents and feeds them to an LLM.")
    service.mark_question_complete(session)
    service.move_to_next_question(session)

    next_q = service.get_current_question(session)
    assert next_q.main_question == "What are embeddings?"