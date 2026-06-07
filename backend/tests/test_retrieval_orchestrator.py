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

from app.services.interview.retrieval_orchestrator import (
    RetrievalOrchestrator,
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

interview_plan = (
    InterviewPlannerService()
    .build_plan(
        target_role="GenAI Engineer",
        candidate_profile=profile,
    )
)

query_plan = (
    QueryPlannerService()
    .build_query_plan(
        role="GenAI Engineer",
        interview_plan=interview_plan,
    )
)

context = (
    RetrievalOrchestrator()
    .build_context(
        query_plan
    )
)

print(
    context.model_dump_json(
        indent=2
    )
)