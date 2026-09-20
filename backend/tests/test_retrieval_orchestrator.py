from pathlib import Path
import json

from app.models.schemas.candidate_profile import CandidateProfile
from app.services.interview.interview_planner_service import InterviewPlannerService
from app.services.interview.query_planner_service import QueryPlannerService
from app.services.interview.retrieval_orchestrator import RetrievalOrchestrator


def test_retrieval_orchestrator():
    profile = CandidateProfile(
        candidate_summary="AI Engineer with RAG and LLM experience",
        skills=["Python", "RAG", "FAISS"],
        claimed_competencies=["Retrieval-Augmented Generation"],
        experience_level="intermediate",
        strengths=["System Architecture"],
    )
    interview_plan = InterviewPlannerService().build_plan(
        target_role="AI/ML Engineer",
        candidate_profile=profile,
        num_questions=1,
    )
    query_plan = QueryPlannerService().build_query_plan(
        role="AI/ML Engineer",
        interview_plan=interview_plan,
    )
    context = RetrievalOrchestrator().build_context(query_plan)
    assert context is not None
    assert len(context.topic_packets) > 0


if __name__ == "__main__":
    sample_path = Path(__file__).resolve().parent.parent / "sample_candidate_profile.json"
    with open(sample_path, "r", encoding="utf-8") as f:
        profile_data = json.load(f)
    profile = CandidateProfile.model_validate(profile_data)
    interview_plan = InterviewPlannerService().build_plan(
        target_role="GenAI Engineer",
        candidate_profile=profile,
    )
    query_plan = QueryPlannerService().build_query_plan(
        role="GenAI Engineer",
        interview_plan=interview_plan,
    )
    context = RetrievalOrchestrator().build_context(query_plan)
    print(context.model_dump_json(indent=2))