from typing import Optional
from pydantic import BaseModel, Field
from app.models.schemas.evidence import EvidenceItem


class InterviewProfile(BaseModel):
    """
    Central domain concept connecting candidate background, target opportunity,
    stage- and nature-aware interview constraints, and provenance evidence.
    """
    company: str = Field(description="Target company name, e.g. 'Stripe', 'Google'")
    target_role: str = Field(description="Target job title, e.g. 'Senior Backend Engineer'")
    interview_stage: str = Field(
        default="Technical Round 1",
        description="Interview stage, e.g. 'Screening', 'Technical Round 1', 'System Design', 'Hiring Manager', 'Final Round'",
    )
    interview_nature: str = Field(
        default="ML/AI Technical",
        description="Nature/type of round, e.g. 'Coding', 'ML/AI Technical', 'System Design', 'Behavioral', 'Domain Specific'",
    )
    focus_areas: list[str] = Field(
        default_factory=list,
        description="Key technical or behavioral competencies prioritized for this round",
    )
    question_style: str = Field(
        default="conversational_technical",
        description="Style of questioning, e.g. 'hands_on_coding', 'system_architecture', 'star_behavioral'",
    )
    difficulty: str = Field(
        default="intermediate",
        description="Expected difficulty level: 'junior', 'intermediate', 'senior', 'staff'",
    )
    number_of_questions: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Desired count of primary questions",
    )
    number_of_followups: int = Field(
        default=1,
        ge=0,
        le=3,
        description="Maximum adaptive follow-ups per primary question",
    )
    rubric_criteria: list[str] = Field(
        default_factory=list,
        description="Stage/nature specific evaluation criteria applied to candidate answers",
    )
    company_insights: list[str] = Field(
        default_factory=list,
        description="Company-specific interview patterns, tech stack facts, or cultural values",
    )
    job_description_snippet: Optional[str] = Field(
        default=None,
        description="Job description excerpt or summary provided by candidate",
    )
    supporting_evidence: list[EvidenceItem] = Field(
        default_factory=list,
        description="Source-backed evidence used to construct this profile",
    )
