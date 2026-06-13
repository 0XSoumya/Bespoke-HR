from pydantic import (
    BaseModel,
)


class CreateInterviewRequest(
    BaseModel
):
    candidate_id: str

    role: str