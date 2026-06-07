from pydantic import BaseModel, Field
from typing import List


class Project(BaseModel):
    title: str
    description: str


class CandidateProfile(BaseModel):
    candidate_summary: str

    skills: List[str] = Field(default_factory=list)

    projects: List[Project] = Field(default_factory=list)

    domains: List[str] = Field(default_factory=list)

    claimed_competencies: List[str] = Field(default_factory=list)

    experience_level: str

    education: List[str] = Field(default_factory=list)

    strengths: List[str] = Field(default_factory=list)