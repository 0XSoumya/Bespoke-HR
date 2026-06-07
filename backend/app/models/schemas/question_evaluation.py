from pydantic import BaseModel, Field


class QuestionEvaluation(
    BaseModel
):
    score: float

    conceptual_accuracy: float

    completeness: float

    technical_depth: float

    communication: float

    strengths: list[str] = Field(
        default_factory=list
    )

    weaknesses: list[str] = Field(
        default_factory=list
    )

    missed_concepts: list[
        str
    ] = Field(
        default_factory=list
    )

    summary: str