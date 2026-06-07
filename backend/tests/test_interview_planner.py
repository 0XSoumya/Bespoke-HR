import json

from app.models.schemas.candidate_profile import (
    CandidateProfile,
)

from app.services.interview.interview_planner_service import (
    InterviewPlannerService,
)


with open(
    "sample_candidate_profile.json",
    "r",
    encoding="utf-8",
) as f:

    profile_data = json.load(f)

profile = CandidateProfile.model_validate(
    profile_data
)

planner = InterviewPlannerService()

plan = planner.build_plan(
    target_role="GenAI Engineer",
    candidate_profile=profile,
)

print(
    plan.model_dump_json(
        indent=2
    )
)