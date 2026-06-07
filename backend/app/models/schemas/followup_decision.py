from pydantic import BaseModel


class FollowupDecision(
    BaseModel
):
    generate_followup: bool

    followup_question: str = ""

    reason: str