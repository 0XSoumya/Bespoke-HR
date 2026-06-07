from pydantic import BaseModel, Field
from app.models.schemas.question_evaluation import (
    QuestionEvaluation,
)

class FollowUpRecord(BaseModel):
    question: str
    answer: str = ""


class QuestionRecord(BaseModel):
    question_id: str

    topic: str

    difficulty: str

    main_question: str

    expected_concepts: list[
        str
    ] = Field(default_factory=list)

    evaluation_criteria: list[
        str
    ] = Field(default_factory=list)

    main_answer: str = ""

    followups: list[
        FollowUpRecord
    ] = Field(default_factory=list)

    evaluation: (
    QuestionEvaluation | None
    ) = None

    completed: bool = False