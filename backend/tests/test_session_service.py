from app.models.schemas.question_set import (
    QuestionSet,
)

from app.models.schemas.interview_question import (
    InterviewQuestion,
)

from app.services.interview.session_service import (
    SessionService,
)


question_set = QuestionSet(
    role="GenAI Engineer",
    questions=[
        InterviewQuestion(
            question_id="q1",
            topic="RAG",
            difficulty="intermediate",
            question=(
                "Explain the key "
                "components of a "
                "RAG pipeline."
            ),
        ),
        InterviewQuestion(
            question_id="q2",
            topic="Embeddings",
            difficulty="intermediate",
            question=(
                "What are embeddings?"
            ),
        ),
    ],
)

service = SessionService()

session = (
    service.create_session(
        question_set
    )
)

print(
    "INTERVIEW ID:",
    session.interview_id
)

current = (
    service.get_current_question(
        session
    )
)

print(
    "\nCURRENT QUESTION:\n"
)

print(
    current.main_question
)

service.save_main_answer(
    session,
    "Sample Answer",
)

service.mark_question_complete(
    session
)

service.move_to_next_question(
    session
)

current = (
    service.get_current_question(
        session
    )
)

print(
    "\nNEXT QUESTION:\n"
)

print(
    current.main_question
)