import pytest
import uuid
from unittest.mock import patch
import httpx

from app.main import app
from app.models.schemas.candidate_profile import CandidateProfile
from app.models.schemas.interview_profile import InterviewProfile
from app.models.schemas.question_record import QuestionRecord
from app.models.schemas.interview_session import InterviewSession
from app.models.schemas.interview_state import InterviewState
from app.models.schemas.interview_report import InterviewReport, PreparationReport, CandidateReport, RecruiterReport
from app.repositories.candidate_repository import CandidateRepository
from app.services.interview.interview_service import InterviewService


@pytest.mark.asyncio
async def test_auth_register_and_login_flow():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        unique_email = f"candidate_{uuid.uuid4().hex[:8]}@example.com"
        reg_payload = {
            "email": unique_email,
            "password": "SecurePassword123!",
            "full_name": "Test Candidate",
            "role": "candidate",
        }
        reg_res = await ac.post("/auth/register", json=reg_payload)
        assert reg_res.status_code == 201
        data = reg_res.json()
        assert "access_token" in data
        assert data["user"]["email"] == unique_email
        assert data["user"]["role"] == "candidate"

        # Login
        login_payload = {
            "email": unique_email,
            "password": "SecurePassword123!",
        }
        login_res = await ac.post("/auth/login", json=login_payload)
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]

        # Verify /auth/me
        me_res = await ac.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_res.status_code == 200
        assert me_res.json()["email"] == unique_email


@pytest.mark.asyncio
async def test_candidate_interview_ownership_and_preparation_flow():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        cand_repo = CandidateRepository()
        cand_id = f"test_cand_{uuid.uuid4().hex[:8]}"

        sample_profile = {
            "candidate_summary": "Full Stack & AI Engineer",
            "skills": ["Python", "FastAPI", "React", "Docker"],
            "projects": [{"title": "AI Assistant", "description": "RAG tool"}],
            "domains": ["AI", "Web"],
            "claimed_competencies": ["API Architecture", "RAG"],
            "experience_level": "intermediate",
            "education": ["B.Tech Computer Science"],
            "strengths": ["System Design", "Problem Solving"],
        }

        # Register candidate A
        cand_a_email = f"cand_a_{uuid.uuid4().hex[:8]}@example.com"
        reg_a = await ac.post("/auth/register", json={
            "email": cand_a_email,
            "password": "Password123!",
            "full_name": "Candidate Alpha",
            "role": "candidate",
        })
        token_a = reg_a.json()["access_token"]
        user_a_id = reg_a.json()["user"]["id"]

        # Register candidate B
        cand_b_email = f"cand_b_{uuid.uuid4().hex[:8]}@example.com"
        reg_b = await ac.post("/auth/register", json={
            "email": cand_b_email,
            "password": "Password123!",
            "full_name": "Candidate Beta",
            "role": "candidate",
        })
        token_b = reg_b.json()["access_token"]

        # Save candidate profile associated with Candidate A
        cand_id = await cand_repo.create_candidate(
            target_role="Backend Engineer",
            resume_filename="resume.pdf",
            resume_text="Resume content",
            candidate_profile=sample_profile,
            user_id=user_a_id,
            candidate_name="Candidate Alpha",
        )

        # Test profile preview
        preview_res = await ac.post(
            "/interviews/profile-preview",
            headers={"Authorization": f"Bearer {token_a}"},
            json={
                "candidate_id": cand_id,
                "role": "Backend Engineer",
                "company": "Stripe",
                "interview_stage": "Technical Round 1",
                "interview_nature": "Coding",
                "number_of_questions": 2,
                "number_of_followups": 1,
            },
        )
        assert preview_res.status_code == 200
        preview_data = preview_res.json()
        assert preview_data["company"] == "Stripe"
        assert preview_data["interview_nature"] == "Coding"
        assert len(preview_data["rubric_criteria"]) > 0

        # Mock interview engine to avoid live Groq generation during API route test
        mock_interview_id = f"int_{uuid.uuid4().hex[:8]}"
        mock_question = QuestionRecord(
            question_id="q1",
            topic="API Design",
            difficulty="intermediate",
            main_question="How would you design an idempotent payment webhook?",
            expected_concepts=["idempotency key", "retry mechanism"],
            evaluation_criteria=["correctness", "clarity"],
        )
        mock_session = InterviewSession(
            interview_id=mock_interview_id,
            question_records=[mock_question],
        )
        mock_profile = CandidateProfile.model_validate(sample_profile)
        mock_interview_profile = InterviewProfile(
            company="Stripe",
            target_role="Backend Engineer",
            interview_stage="Technical Round 1",
            interview_nature="Coding",
            number_of_questions=1,
            number_of_followups=1,
        )
        mock_state = InterviewState(
            candidate_id=cand_id,
            role="Backend Engineer",
            company="Stripe",
            interview_profile=mock_interview_profile,
            candidate_profile=mock_profile,
            session=mock_session,
            current_question=mock_question,
            candidate_user_id=user_a_id,
            candidate_email=cand_a_email,
            status="interview_created",
            number_of_questions=1,
        )

        with patch.object(InterviewService, "create_interview", return_value=mock_state):
            create_res = await ac.post(
                "/interviews/create",
                headers={"Authorization": f"Bearer {token_a}"},
                json={
                    "candidate_id": cand_id,
                    "role": "Backend Engineer",
                    "company": "Stripe",
                    "interview_stage": "Technical Round 1",
                    "interview_nature": "Coding",
                    "number_of_questions": 1,
                    "number_of_followups": 1,
                },
            )
            assert create_res.status_code == 200
            int_data = create_res.json()
            assert int_data["interview_id"] == mock_interview_id
            assert int_data["company"] == "Stripe"

        # Save mock state to database directly for authorization & report test
        await cand_repo.collection.database.interviews.insert_one({
            "_id": mock_interview_id,
            "candidate_id": cand_id,
            "candidate_user_id": user_a_id,
            "candidate_email": cand_a_email,
            "company": "Stripe",
            "role": "Backend Engineer",
            "status": "completed",
            "state": mock_state.model_dump(),
        })

        # Test 1: Candidate A can access their interview
        get_res_a = await ac.get(
            f"/interviews/{mock_interview_id}",
            headers={"Authorization": f"Bearer {token_a}"},
        )
        assert get_res_a.status_code == 200

        # Test 2: Candidate B is FORBIDDEN (Strict Ownership check)
        get_res_b = await ac.get(
            f"/interviews/{mock_interview_id}",
            headers={"Authorization": f"Bearer {token_b}"},
        )
        assert get_res_b.status_code == 403

        # Test 3: Unauthenticated user is rejected with 401
        get_res_anon = await ac.get(f"/interviews/{mock_interview_id}")
        assert get_res_anon.status_code == 401

        # Test 4: Report access excludes recruiter report for candidate
        mock_report = InterviewReport(
            preparation_report=PreparationReport(
                overall_readiness_score=8.5,
                readiness_tier="Strong Baseline",
                executive_summary="Solid readiness for Stripe.",
                strengths=["Idempotency knowledge"],
                priority_gaps=["Concurrency tuning"],
                topic_breakdown={"API Design": 8.5},
                recommended_actions=["Review webhook signature verification"],
            ),
            candidate_report=CandidateReport(
                overall_score=8.5,
                strengths=["Idempotency knowledge"],
                areas_for_improvement=["Concurrency tuning"],
                learning_recommendations=["Review webhook signature verification"],
                summary="Solid readiness for Stripe.",
            ),
            recruiter_report=RecruiterReport(
                overall_score=8.5,
                recommendation="Hire",
                summary="Internal recruiter evaluation note",
            ),
        )

        with patch.object(InterviewService, "get_report", return_value=mock_report):
            rep_res = await ac.get(
                f"/interviews/{mock_interview_id}/report",
                headers={"Authorization": f"Bearer {token_a}"},
            )
            assert rep_res.status_code == 200
            rep_data = rep_res.json()
            assert "preparation_report" in rep_data
            assert rep_data["preparation_report"]["readiness_tier"] == "Strong Baseline"
            assert "candidate_report" in rep_data
            # Recruiter report MUST NOT be exposed to candidate
            assert "recruiter_report" not in rep_data
