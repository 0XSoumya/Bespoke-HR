from pydantic import (
    BaseModel,
)


class SubmitAnswerRequest(
    BaseModel
):
    answer: str