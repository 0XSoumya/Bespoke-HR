from pydantic import BaseModel, Field


class RecruiterReport(
    BaseModel
):
    overall_score: float

    topic_scores: dict[
        str,
        float
    ]

    strengths: list[
        str
    ] = Field(default_factory=list)

    weaknesses: list[
        str
    ] = Field(default_factory=list)

    recommendation: str

    summary: str


class CandidateReport(
    BaseModel
):
    overall_score: float

    strengths: list[
        str
    ] = Field(default_factory=list)

    areas_for_improvement: list[
        str
    ] = Field(default_factory=list)

    learning_recommendations: list[
        str
    ] = Field(default_factory=list)

    summary: str


class InterviewReport(
    BaseModel
):
    recruiter_report: RecruiterReport

    candidate_report: CandidateReport