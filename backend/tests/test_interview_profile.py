from app.models.schemas.candidate_profile import CandidateProfile
from app.services.interview.interview_profile_service import InterviewProfileService


def test_interview_profile_curated_company():
    service = InterviewProfileService()
    profile = CandidateProfile(
        candidate_summary="Software engineer specializing in payment APIs and distributed systems.",
        skills=["Python", "Go", "PostgreSQL", "Kafka"],
        claimed_competencies=["Distributed systems", "API design"],
        experience_level="senior",
        strengths=["System reliability"],
    )

    interview_profile = service.build_interview_profile(
        candidate_profile=profile,
        company="Stripe",
        target_role="Senior Backend Engineer",
        interview_stage="System Design",
        interview_nature="System Design",
        number_of_questions=3,
        number_of_followups=2,
        job_description="Design high-volume idempotency and payment settlement pipelines.",
    )

    assert interview_profile.company == "Stripe"
    assert interview_profile.target_role == "Senior Backend Engineer"
    assert interview_profile.interview_stage == "System Design"
    assert interview_profile.interview_nature == "System Design"
    assert interview_profile.number_of_questions == 3
    assert interview_profile.number_of_followups == 2
    assert len(interview_profile.company_insights) > 0
    assert len(interview_profile.rubric_criteria) > 0
    assert len(interview_profile.supporting_evidence) >= 3  # Company + Resume + JD


def test_interview_profile_custom_company_fallback():
    service = InterviewProfileService()
    profile = CandidateProfile(
        candidate_summary="Frontend and AI engineer",
        skills=["React", "TypeScript", "Python"],
        claimed_competencies=["Web interfaces"],
        experience_level="intermediate",
        strengths=["User experience"],
    )

    interview_profile = service.build_interview_profile(
        candidate_profile=profile,
        company="Acme AI Startup",
        target_role="Full Stack AI Engineer",
        interview_stage="Technical Round 1",
        interview_nature="Coding",
    )

    assert interview_profile.company == "Acme AI Startup"
    assert len(interview_profile.rubric_criteria) > 0
    assert len(interview_profile.supporting_evidence) >= 1
