from pydantic import BaseModel, Field
from typing import List


class TopicQueryPlan(BaseModel):
    topic: str

    priority: int

    difficulty: str

    queries: List[str] = Field(
        default_factory=list
    )

    focus_areas: List[str] = Field(
        default_factory=list
    )

    question_objectives: List[str] = Field(
        default_factory=list
    )


class QueryPlan(BaseModel):
    role: str

    topic_plans: List[TopicQueryPlan]