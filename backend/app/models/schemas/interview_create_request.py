from typing import Optional
from pydantic import BaseModel, Field


class CreateInterviewRequest(BaseModel):
    candidate_id: str
    role: str
    number_of_questions: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of main interview questions to generate and assess",
    )
    candidate_user_id: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_name: Optional[str] = None
    scheduled_at: Optional[str] = None