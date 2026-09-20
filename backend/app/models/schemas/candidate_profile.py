from typing import Any, List, Optional, Union
from pydantic import BaseModel, Field, field_validator


class Project(BaseModel):
    title: str
    description: str


class EducationItem(BaseModel):
    degree: Optional[str] = None
    field: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[Union[str, int]] = None

    def to_display_string(self) -> str:
        parts = [p for p in [self.degree, self.field, self.institution, str(self.year) if self.year else None] if p]
        return " - ".join(parts) if parts else "Higher Education"


class CandidateProfile(BaseModel):
    candidate_summary: str

    skills: List[str] = Field(default_factory=list)

    projects: List[Project] = Field(default_factory=list)

    domains: List[str] = Field(default_factory=list)

    claimed_competencies: List[str] = Field(default_factory=list)

    experience_level: str

    education: List[Union[str, EducationItem, dict[str, Any]]] = Field(default_factory=list)

    strengths: List[str] = Field(default_factory=list)

    @field_validator("education", mode="before")
    @classmethod
    def normalize_education(cls, v: Any) -> Any:
        if isinstance(v, str):
            return [v]
        return v