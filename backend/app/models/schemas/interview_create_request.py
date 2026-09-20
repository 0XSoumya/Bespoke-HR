from typing import Optional
from pydantic import BaseModel, Field


class CreateInterviewRequest(BaseModel):
    candidate_id: str
    role: str = Field(description="Target role title, e.g. 'Backend Engineer'")
    company: str = Field(default="Target Company", description="Company being interviewed for")
    job_description: Optional[str] = Field(default=None, description="Job description text or summary")
    interview_stage: str = Field(
        default="Technical Round 1",
        description="Stage: 'Screening', 'Technical Round 1', 'System Design', 'Hiring Manager', 'Behavioral', 'Final Round'",
    )
    interview_nature: str = Field(
        default="ML/AI Technical",
        description="Nature: 'Coding', 'ML/AI Technical', 'System Design', 'Behavioral', 'Domain Specific'",
    )
    number_of_questions: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of main interview questions to generate and assess",
    )
    number_of_followups: int = Field(
        default=1,
        ge=0,
        le=3,
        description="Maximum adaptive follow-ups per main question",
    )
    candidate_user_id: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_name: Optional[str] = None
    scheduled_at: Optional[str] = None