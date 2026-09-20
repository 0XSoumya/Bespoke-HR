from pathlib import Path
from unittest.mock import patch
import json

from app.models.schemas.candidate_profile import CandidateProfile
from app.models.schemas.question_set import QuestionSet
from app.models.schemas.interview_question import InterviewQuestion
from app.services.interview.interview_planner_service import InterviewPlannerService
from app.services.interview.query_planner_service import QueryPlannerService
from app.services.interview.retrieval_orchestrator import RetrievalOrchestrator
from app.services.interview.question_generator_service import QuestionGeneratorService


def test_question_generation_with_mock():
    profile = CandidateProfile(
        candidate_summary="AI Engineer with RAG experience",
        skills=["Python", "RAG"],
        claimed_competencies=["RAG"],
        experience_level="intermediate",
        strengths=["System Design"],
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
    retrieval_context = RetrievalOrchestrator().build_context(query_plan)

    mock_qset = QuestionSet(
        role="AI/ML Engineer",
        questions=[
            InterviewQuestion(
                question_id="q1",
                topic="RAG",
                difficulty="intermediate",
                question="How does retrieval augmented generation work?",
                expected_concepts=["retriever", "generator"],
                evaluation_criteria=["accuracy", "clarity"],
            )
        ],
    )

    with patch.object(QuestionGeneratorService, "generate_questions", return_value=mock_qset):
        generator = QuestionGeneratorService()
        qset = generator.generate_questions(retrieval_context)
        assert len(qset.questions) == 1
        assert qset.questions[0].topic == "RAG"


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
    retrieval_context = RetrievalOrchestrator().build_context(query_plan)
    question_set = QuestionGeneratorService().generate_questions(retrieval_context)
    print(question_set.model_dump_json(indent=2))