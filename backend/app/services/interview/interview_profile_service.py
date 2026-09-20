from typing import Optional
from app.models.schemas.interview_profile import InterviewProfile
from app.models.schemas.candidate_profile import CandidateProfile
from app.models.schemas.evidence import EvidenceItem
from app.services.interview.company_intelligence_service import CompanyIntelligenceService


class InterviewProfileService:
    """
    Constructs the canonical Interview Profile by unifying Candidate Profile,
    Job Description context, Company Interview Intelligence, and Stage/Nature constraints.
    """

    def __init__(self):
        self.company_intel_service = CompanyIntelligenceService()

    def build_interview_profile(
        self,
        candidate_profile: CandidateProfile,
        company: str,
        target_role: str,
        interview_stage: str = "Technical Round 1",
        interview_nature: str = "ML/AI Technical",
        number_of_questions: int = 3,
        number_of_followups: int = 1,
        job_description: Optional[str] = None,
    ) -> InterviewProfile:
        # 1. Fetch company interview intelligence & evidence
        insights, company_evidence, rubric = self.company_intel_service.get_company_intelligence(
            company=company,
            target_role=target_role,
            interview_stage=interview_stage,
            interview_nature=interview_nature,
            job_description=job_description,
        )

        all_evidence: list[EvidenceItem] = list(company_evidence)

        # 2. Add Candidate evidence
        if candidate_profile.candidate_summary:
            all_evidence.append(
                EvidenceItem(
                    source_type="candidate_resume",
                    title="Candidate Resume Summary",
                    content=candidate_profile.candidate_summary[:500],
                    confidence=1.0,
                )
            )

        # 3. Add JD evidence if available
        jd_snippet = None
        if job_description and job_description.strip():
            clean_jd = job_description.strip()
            jd_snippet = clean_jd[:500] + ("..." if len(clean_jd) > 500 else "")
            all_evidence.append(
                EvidenceItem(
                    source_type="job_description",
                    title=f"{company} Job Description Requirements",
                    content=jd_snippet,
                    confidence=1.0,
                )
            )

        # 4. Determine focus areas based on role, candidate claimed competencies, and nature
        focus_areas: list[str] = []

        # Start with candidate competencies that overlap with role or common topics
        if candidate_profile.claimed_competencies:
            focus_areas.extend(candidate_profile.claimed_competencies[:3])
        elif candidate_profile.skills:
            focus_areas.extend(candidate_profile.skills[:3])

        # Add nature-specific focus areas if not already covered
        nature_defaults = {
            "Coding": ["Data structures", "Algorithmic complexity", "Clean implementation"],
            "ML/AI Technical": ["RAG Architecture", "Model Evaluation", "Inference Optimization"],
            "System Design": ["Distributed Systems", "Scalability & Bottlenecks", "Data Modeling"],
            "Behavioral": ["Leadership Principles", "Conflict Resolution", "Project Ownership"],
            "Domain Specific": ["Domain Fundamentals", "Industry Standards", "System Architecture"],
        }
        for default_focus in nature_defaults.get(interview_nature, ["Core Technical Skills"]):
            if default_focus not in focus_areas:
                focus_areas.append(default_focus)

        # 5. Determine question style
        style_map = {
            "Coding": "hands_on_problem_solving",
            "ML/AI Technical": "deep_dive_conceptual_and_architectural",
            "System Design": "open_ended_architecture_and_tradeoffs",
            "Behavioral": "star_behavioral_inquiry",
            "Domain Specific": "applied_scenario_analysis",
        }
        question_style = style_map.get(interview_nature, "conversational_technical")

        # 6. Determine difficulty
        difficulty = candidate_profile.experience_level or "intermediate"

        return InterviewProfile(
            company=company,
            target_role=target_role,
            interview_stage=interview_stage,
            interview_nature=interview_nature,
            focus_areas=focus_areas[:5],
            question_style=question_style,
            difficulty=difficulty,
            number_of_questions=max(1, min(number_of_questions, 10)),
            number_of_followups=max(0, min(number_of_followups, 3)),
            rubric_criteria=rubric,
            company_insights=insights,
            job_description_snippet=jd_snippet,
            supporting_evidence=all_evidence,
        )
