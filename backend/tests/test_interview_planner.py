from pathlib import Path
import json

from app.models.schemas.candidate_profile import CandidateProfile
from app.services.interview.interview_planner_service import InterviewPlannerService


def test_interview_planner_builds_plan():
    profile = CandidateProfile(
        candidate_summary="AI Engineer with RAG and LLM experience",
        skills=["Python", "RAG", "FAISS", "LangChain"],
        claimed_competencies=["Retrieval-Augmented Generation", "Embeddings"],
        experience_level="intermediate",
        strengths=["System Architecture"],
    )
    planner = InterviewPlannerService()
    plan = planner.build_plan(target_role="AI/ML Engineer", candidate_profile=profile, num_questions=3)
    assert plan is not None
    assert plan.role == "AI/ML Engineer"
    assert len(plan.topics) <= 3


if __name__ == "__main__":
    sample_path = Path(__file__).resolve().parent.parent / "sample_candidate_profile.json"
    with open(sample_path, "r", encoding="utf-8") as f:
        profile_data = json.load(f)
    profile = CandidateProfile.model_validate(profile_data)
    planner = InterviewPlannerService()
    plan = planner.build_plan(target_role="GenAI Engineer", candidate_profile=profile)
    print(plan.model_dump_json(indent=2))