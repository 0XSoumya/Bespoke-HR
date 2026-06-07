from pydantic import BaseModel, Field
from typing import Any, Dict, List


class RetrievedChunk(BaseModel):
    chunk: str

    metadata: Dict[str, Any]

    retrieval_count: int


class TopicContextPacket(BaseModel):
    topic: str

    focus_areas: List[str] = Field(
        default_factory=list
    )

    question_objectives: List[str] = Field(
        default_factory=list
    )

    retrieved_chunks: List[
        RetrievedChunk
    ] = Field(default_factory=list)


class RetrievalContext(BaseModel):
    role: str

    topic_packets: List[
        TopicContextPacket
    ] = Field(default_factory=list)