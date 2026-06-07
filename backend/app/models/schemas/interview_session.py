from pydantic import BaseModel, Field

from app.models.schemas.question_record import (
    QuestionRecord,
)


class InterviewSession(BaseModel):
    interview_id: str

    current_question_index: int = 0

    status: str = "in_progress"

    question_records: list[
        QuestionRecord
    ] = Field(default_factory=list)