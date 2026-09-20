# Roadmap

## Phase 1: Product-pivot architecture and data-model cleanup [COMPLETED]
- Status: Completed
- Major deliverables:
  - Canonical `InterviewProfile` and `EvidenceItem` schemas (`backend/app/models/schemas/interview_profile.py`, `backend/app/models/schemas/evidence.py`).
  - Distinction established between candidate profile, Interview Profile, and interview session state.
  - Candidate preparation report schema (`backend/app/models/schemas/interview_report.py`).

## Phase 2: Authentication and candidate access [COMPLETED]
- Status: Completed
- Major deliverables:
  - Candidate authentication (`/auth/register`, `/auth/login`, `/auth/me`).
  - Candidate ownership enforcement: strict 401 unauthenticated and 403 cross-candidate blocking in `backend/app/api/routes/interview.py`.
  - Recruiter-specific reports isolated and hidden from candidates.

## Phase 3: Candidate onboarding and intake [COMPLETED]
- Status: Completed
- Major deliverables:
  - Resume PDF parsing (`/resume/upload`) extracting candidate summary, competencies, skills, projects, and domain depth.
  - Candidate preparation intake capturing company, role, JD snippet, interview stage, round nature, and question/follow-up settings.

## Phase 4: Interview Profile creation [COMPLETED]
- Status: Completed
- Major deliverables:
  - Canonical InterviewProfile synthesized via `backend/app/services/interview/interview_profile_service.py`.
  - Preview endpoint `POST /interviews/profile-preview` providing candidates with transparent view of company insights, focus areas, and rubric criteria before launching.

## Phase 5: Interview creation and planning [COMPLETED]
- Status: Completed
- Major deliverables:
  - Blended role and nature configurations (`NATURE_CONFIGS` in `role_config.py`).
  - Candidate-specified question counts and follow-up limits injected into LangGraph execution plan.

## Phase 6: End-to-end interview UI [COMPLETED]
- Status: Completed
- Major deliverables:
  - Next.js 16 frontend with Tailwind CSS v4, Lucide icons, Geist fonts, and dark/light mode toggle.
  - `InterviewSessionView`: Conversation stream, code mode, focus hint toggles, keyboard shortcuts (Cmd+Enter).
  - API rewrites and typed API client (`frontend/lib/api.ts`).

## Phase 7: Adaptive follow-ups and answer progression [COMPLETED]
- Status: Completed
- Major deliverables:
  - Configurable follow-up budget (0-3 follow-ups per question) enforced in `followup_service.py` and LangGraph interview workflow.
  - Adaptive follow-up generation evaluating candidate answers and generating targeted technical probes.

## Phase 8: Evaluation and scoring adjustments [COMPLETED]
- Status: Completed
- Major deliverables:
  - Stage- and nature-calibrated rubric scoring (Coding, System Design, ML/AI Technical, Behavioral) in `evaluation_service.py` and `evaluation_prompt.py`.
  - Evidence extraction from candidate answers and fallback topic packets for LLM robustness.

## Phase 9: Preparation report [COMPLETED]
- Status: Completed
- Major deliverables:
  - `PreparationReport`: Readiness score (0-10), readiness tier classification, strengths, priority gaps, rubric dimension breakdown, actionable practice roadmap, and question reviews.
  - Candidate frontend report view (`PreparationReportView`) with print support.

## Phase 10: Company-specific research and knowledge enrichment [COMPLETED]
- Status: Completed
- Major deliverables:
  - `CompanyIntelligenceService`: Multi-tier engine with curated intelligence for Stripe, Google, Meta, Amazon, OpenAI, Anthropic + resilient live research synthesis for arbitrary companies.
  - Grounded evidence citations with confidence scores and provenance metadata.

## Phase 11: Production hardening & test automation [COMPLETED]
- Status: Completed
- Major deliverables:
  - `DatabaseProxy` dynamic client in `backend/app/core/database.py` resolving Motor asyncio event loop closures.
  - Comprehensive candidate flow test suite (`backend/tests/test_candidate_api_flow.py`).
  - 15/15 backend pytest suite passing.
  - Frontend TypeScript verification and Next.js 16 production build passing (`npm run build`).

## Phase 12: Production deployment & telemetry [NEXT]
- Ongoing hardening:
  - Production containerization with Docker Compose.
  - Telemetry and tracing for LLM latency.
