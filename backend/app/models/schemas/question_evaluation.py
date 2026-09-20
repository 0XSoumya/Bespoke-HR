from pydantic import BaseModel, Field


class QuestionEvaluation(BaseModel):
    score: float = 0.0

    conceptual_accuracy: float = 0.0

    completeness: float = 0.0

    technical_depth: float = 0.0

    communication: float = 0.0

    rubric_scores: dict[str, float] = Field(
        default_factory=dict,
        description="Stage/nature specific rubric criteria scores (e.g. correctness, scalability, ownership)",
    )

    strengths: list[str] = Field(default_factory=list)

    weaknesses: list[str] = Field(default_factory=list)

    missed_concepts: list[str] = Field(default_factory=list)

    evidence: list[str] = Field(
        default_factory=list,
        description="Quotes or specific factual evidence from the candidate answer",
    )

    summary: str = ""