import uuid

from app.models.schemas.interview_session import (
    InterviewSession,
)

from app.models.schemas.question_record import (
    QuestionRecord,
    FollowUpRecord,
)


class SessionService:

    def create_session(
        self,
        question_set,
    ) -> InterviewSession:

        records = []

        for question in (
            question_set.questions
        ):

            records.append(
                QuestionRecord(
                    question_id=question.question_id,
                    topic=question.topic,
                    difficulty=question.difficulty,
                    main_question=question.question,
                    expected_concepts=(
                        question.expected_concepts
                    ),
                    evaluation_criteria=(
                        question.evaluation_criteria
                    ),
                )
            )

        return InterviewSession(
            interview_id=str(
                uuid.uuid4()
            ),
            question_records=records,
        )

    def get_current_question(
        self,
        session: InterviewSession,
    ):

        if (
            session.current_question_index
            >= len(
                session.question_records
            )
        ):
            return None

        return (
            session.question_records[
                session.current_question_index
            ]
        )

    def move_to_next_question(
        self,
        session: InterviewSession,
    ):

        session.current_question_index += 1

        if (
            session.current_question_index
            >= len(
                session.question_records
            )
        ):
            session.status = (
                "completed"
            )

        return session

    def save_main_answer(
        self,
        session: InterviewSession,
        answer: str,
    ):

        question = (
            self.get_current_question(
                session
            )
        )

        question.main_answer = (
            answer
        )

        return session

    def add_followup_question(
        self,
        session: InterviewSession,
        followup_question: str,
    ):

        question = (
            self.get_current_question(
                session
            )
        )

        question.followups.append(
            FollowUpRecord(
                question=(
                    followup_question
                )
            )
        )

        return session

    def save_followup_answer(
        self,
        session: InterviewSession,
        answer: str,
    ):

        question = (
            self.get_current_question(
                session
            )
        )

        if not question.followups:
            raise ValueError(
                "No followup exists."
            )

        question.followups[
            -1
        ].answer = answer

        return session

    def get_latest_followup(
        self,
        session: InterviewSession,
    ):

        question = (
            self.get_current_question(
                session
            )
        )

        if not question.followups:
            return None

        return question.followups[
            -1
        ]

    def mark_question_complete(
        self,   
        session: InterviewSession,
    ):

        question = (
            self.get_current_question(
                session
            )
        )

        question.completed = True

        return session