from pydantic import BaseModel
from typing import List


class InterviewTopic(BaseModel):
    topic: str
    priority: int
    difficulty: str
    source: str


class InterviewPlan(BaseModel):
    role: str
    topics: List[InterviewTopic]