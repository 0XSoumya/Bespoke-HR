from pydantic import BaseModel, Field

from app.models.schemas.interview_question import (
    InterviewQuestion,
)


class QuestionSet(BaseModel):
    role: str

    questions: list[
        InterviewQuestion
    ] = Field(default_factory=list)