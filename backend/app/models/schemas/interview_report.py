from typing import Any, Optional
from pydantic import BaseModel, Field
from app.models.schemas.evidence import EvidenceItem


class RecruiterReport(BaseModel):
    overall_score: float
    topic_scores: dict[str, float] = Field(default_factory=dict)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    recommendation: str = "Candidate assessment completed"
    summary: str = ""


class CandidateReport(BaseModel):
    overall_score: float
    strengths: list[str] = Field(default_factory=list)
    areas_for_improvement: list[str] = Field(default_factory=list)
    learning_recommendations: list[str] = Field(default_factory=list)
    summary: str = ""


class QuestionPreparationReview(BaseModel):
    question_id: str
    topic: str
    main_question: str
    candidate_answer: str = ""
    followups: list[dict[str, str]] = Field(default_factory=list)
    score: float = 0.0
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    model_advice: str = ""
    evidence: list[str] = Field(default_factory=list)


class PreparationReport(BaseModel):
    """
    Candidate-first preparation report centered on readiness, actionable coaching,
    company context, answer-level evidence, and next preparation steps.
    """
    overall_readiness_score: float = Field(
        default=0.0,
        description="Overall readiness score on 0-10 or 0-100 scale",
    )
    readiness_tier: str = Field(
        default="Ready",
        description="Tier: 'Interview Ready', 'Strong Baseline', 'Needs Targeted Practice', 'Early Preparation'",
    )
    executive_summary: str = Field(
        default="",
        description="Encouraging, evidence-grounded summary of candidate readiness for this specific company and round",
    )
    strengths: list[str] = Field(
        default_factory=list,
        description="Key demonstrated competencies and high-scoring areas",
    )
    priority_gaps: list[str] = Field(
        default_factory=list,
        description="High-impact gaps to close before the actual interview",
    )
    topic_breakdown: dict[str, float] = Field(
        default_factory=dict,
        description="Competency scores by topic (0.0 to 10.0)",
    )
    nature_rubric_scores: dict[str, float] = Field(
        default_factory=dict,
        description="Scores on the round's specific rubric dimensions (e.g. system scalability, trade-off analysis)",
    )
    company_context_insights: list[str] = Field(
        default_factory=list,
        description="Target company interview patterns and role expectations highlighted in this session",
    )
    recommended_actions: list[str] = Field(
        default_factory=list,
        description="Actionable, concrete preparation tasks to perform next",
    )
    question_reviews: list[QuestionPreparationReview] = Field(
        default_factory=list,
        description="Detailed review of each question, answer, and follow-up interaction",
    )
    evidence_citations: list[EvidenceItem] = Field(
        default_factory=list,
        description="Provenance sources backing the report recommendations",
    )


class InterviewReport(BaseModel):
    preparation_report: Optional[PreparationReport] = None
    candidate_report: CandidateReport
    recruiter_report: Optional[RecruiterReport] = None