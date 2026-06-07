import json

from app.models.schemas.interview_question import (
    InterviewQuestion,
)

from app.models.schemas.question_set import (
    QuestionSet,
)

from app.services.interview.question_generator_prompt import (
    build_topic_question_prompt,
)

from app.services.llm.groq_service import (
    GroqService,
)


class QuestionGeneratorService:

    def __init__(self):
        self.llm = GroqService()

    def _clean_response(
        self,
        response: str,
    ) -> str:

        cleaned = response.strip()

        if cleaned.startswith(
            "```"
        ):
            cleaned = (
                cleaned.replace(
                    "```json",
                    "",
                )
            )

            cleaned = (
                cleaned.replace(
                    "```",
                    "",
                )
            )

        return cleaned.strip()

    def generate_questions(
        self,
        retrieval_context,
    ) -> QuestionSet:

        questions = []

        question_counter = 1

        for topic_packet in (
            retrieval_context.topic_packets
        ):

            prompt = (
                build_topic_question_prompt(
                    role=(
                        retrieval_context.role
                    ),
                    topic_packet=(
                        topic_packet
                    ),
                )
            )

            response = (
                self.llm.invoke(
                    prompt
                )
            )

            cleaned = (
                self._clean_response(
                    response
                )
            )

            parsed = json.loads(
                cleaned
            )

            for item in parsed[
                "questions"
            ]:

                questions.append(
                    InterviewQuestion(
                        question_id=(
                            f"q{question_counter}"
                        ),
                        topic=item[
                            "topic"
                        ],
                        difficulty=item[
                            "difficulty"
                        ],
                        question=item[
                            "question"
                        ],
                        expected_concepts=(
                            item.get(
                                "expected_concepts",
                                [],
                            )
                        ),
                        evaluation_criteria=(
                            item.get(
                                "evaluation_criteria",
                                [],
                            )
                        ),
                    )
                )

                question_counter += 1

        return QuestionSet(
            role=(
                retrieval_context.role
            ),
            questions=questions,
        )