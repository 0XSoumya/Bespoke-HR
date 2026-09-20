from pathlib import Path
import json

from app.models.schemas.candidate_profile import CandidateProfile
from app.services.interview.interview_planner_service import InterviewPlannerService
from app.services.interview.query_planner_service import QueryPlannerService


def test_query_planner_builds_query_plan():
    profile = CandidateProfile(
        candidate_summary="AI Engineer with RAG and LLM experience",
        skills=["Python", "RAG", "FAISS"],
        claimed_competencies=["Retrieval-Augmented Generation"],
        experience_level="intermediate",
        strengths=["System Architecture"],
    )
    interview_planner = InterviewPlannerService()
    interview_plan = interview_planner.build_plan(
        target_role="AI/ML Engineer",
        candidate_profile=profile,
        num_questions=2,
    )
    query_planner = QueryPlannerService()
    query_plan = query_planner.build_query_plan(
        role="AI/ML Engineer",
        interview_plan=interview_plan,
    )
    assert query_plan is not None
    assert len(query_plan.topic_plans) > 0


if __name__ == "__main__":
    sample_path = Path(__file__).resolve().parent.parent / "sample_candidate_profile.json"
    with open(sample_path, "r", encoding="utf-8") as f:
        profile_data = json.load(f)
    profile = CandidateProfile.model_validate(profile_data)
    interview_planner = InterviewPlannerService()
    interview_plan = interview_planner.build_plan(
        target_role="GenAI Engineer",
        candidate_profile=profile,
    )
    query_planner = QueryPlannerService()
    query_plan = query_planner.build_query_plan(
        role="GenAI Engineer",
        interview_plan=interview_plan,
    )
    print(query_plan.model_dump_json(indent=2))