from pydantic import BaseModel, Field
from typing import List


class InterviewQuestion(BaseModel):
    question_id: str

    topic: str

    difficulty: str

    question: str

    expected_concepts: List[str] = Field(
        default_factory=list
    )

    evaluation_criteria: List[str] = Field(
        default_factory=list
    )