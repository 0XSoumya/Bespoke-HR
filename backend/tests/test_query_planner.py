import json

from app.models.schemas.candidate_profile import (
    CandidateProfile,
)

from app.services.interview.interview_planner_service import (
    InterviewPlannerService,
)

from app.services.interview.query_planner_service import (
    QueryPlannerService,
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

interview_planner = (
    InterviewPlannerService()
)

interview_plan = (
    interview_planner.build_plan(
        target_role="GenAI Engineer",
        candidate_profile=profile,
    )
)

query_planner = (
    QueryPlannerService()
)

query_plan = (
    query_planner.build_query_plan(
        role="GenAI Engineer",
        interview_plan=interview_plan,
    )
)

print(
    query_plan.model_dump_json(
        indent=2
    )
)