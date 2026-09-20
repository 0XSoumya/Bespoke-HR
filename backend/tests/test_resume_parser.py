from app.services.resume.resume_parser_service import ResumeParserService
from app.models.schemas.candidate_profile import CandidateProfile


def test_candidate_profile_validation():
    sample_data = {
        "candidate_summary": "Test engineer with AI and backend expertise.",
        "skills": ["Python", "FastAPI", "MongoDB"],
        "projects": [{"title": "AI Assistant", "description": "Built RAG assistant"}],
        "domains": ["AI", "Search"],
        "claimed_competencies": ["Backend APIs", "RAG"],
        "experience_level": "intermediate",
        "education": [{"degree": "B.Tech", "field": "CS", "institution": None, "year": None}],
        "strengths": ["Quick learner", "API design"],
    }
    profile = CandidateProfile.model_validate(sample_data)
    assert profile.candidate_summary == sample_data["candidate_summary"]
    assert "Python" in profile.skills


def main():
    resume_text = """
    Soumya Sahoo
    B.Tech Computer Science (AI & ML Specialization)
    SKILLS: Python, Machine Learning, Deep Learning, LangChain, LangGraph, FAISS, ChromaDB, FastAPI, MongoDB, Docker, Git, Streamlit, RAG, Prompt Engineering
    """
    service = ResumeParserService()
    profile = service.parse_resume(resume_text=resume_text)
    print("\nCandidate Profile\n", profile.model_dump_json(indent=2))


if __name__ == "__main__":
    main()