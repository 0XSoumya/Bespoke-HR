from datetime import datetime, timezone
from typing import Literal, Optional
from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    """
    Structured provenance record capturing evidence origin, content, and trust level.
    """
    source_type: Literal[
        "candidate_resume",
        "job_description",
        "company_knowledge",
        "internal_technical",
        "live_research",
        "candidate_answer",
        "system_inference",
    ]
    title: str = Field(description="Short human-readable label or header for the evidence source")
    content: str = Field(description="Extracted fact, quote, or summary")
    url: Optional[str] = Field(default=None, description="Source URL if retrieved via web research")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Reliability score 0.0 to 1.0")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
