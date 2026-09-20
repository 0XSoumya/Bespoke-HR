# Project State Snapshot

## Repository status
- Git HEAD: Candidate-first SaaS Pivot Implementation
- Graphify status: Baseline architectural reference available under `graphify-out/`.

## Candidate Preparation Product Architecture
- The application has been fully pivoted from an unintegrated legacy recruiter screening tool into a complete, candidate-first AI interview preparation SaaS platform.
- The pipeline centers on:
  1. Candidate Onboarding & Resume Intake: PDF resume parsing with technical competency extraction (projects, skills, domain depth).
  2. Intake Calibration: Target company, role, JD snippet, interview stage (Screening, Technical Round 1, System Design, Behavioral, Hiring Manager, Final Round), round nature (Coding, System Design, ML/AI Technical, Behavioral), and primary question & follow-up counters.
  3. Canonical `InterviewProfile`: Unified domain model blending candidate context, role expectations, and company-specific interview intelligence.
  4. Company Intelligence Service: Curated company interview memory (Stripe, Google, Meta, Amazon, OpenAI, Anthropic) with live research synthesis fallback and evidence provenance citations.
  5. LangGraph Interview Orchestrator: Dynamic question execution, configurable follow-up budget enforcement (0-3), and stage/nature rubric evaluation.
  6. Preparation Report: Overall readiness score (0-10), readiness tier classification ("Staff / Principal Ready", "Senior Ready", "Strong Baseline", "Targeted Growth Required"), strengths, priority gaps, topic breakdown, action plan roadmap, question-by-question review, and provenance citations.

## Backend Status
- Clean FastAPI architecture with full Pydantic models:
  - `backend/app/models/schemas/interview_profile.py`: Canonical InterviewProfile schema.
  - `backend/app/models/schemas/evidence.py`: EvidenceItem schema with confidence scoring and source tracing.
  - `backend/app/models/schemas/interview_report.py`: PreparationReport schema with readiness score, tier, and question reviews.
  - `backend/app/services/interview/company_intelligence_service.py`: Multi-tier company intelligence engine.
  - `backend/app/services/interview/interview_profile_service.py`: Synthesizes unified interview profiles with citations.
  - `backend/app/services/interview/role_config.py`: Nature configurations for Coding, System Design, ML/AI Technical, and Behavioral rounds.
  - `backend/app/services/interview/evaluation_service.py`: Rubric-based evaluation per stage and nature.
  - `backend/app/core/database.py`: Dynamic `DatabaseProxy` guaranteeing Motor client resilience across event loops.
  - `backend/app/api/routes/interview.py`: Strict ownership authorization (401 unauthenticated, 403 cross-candidate isolation; recruiter reports hidden from candidates).

## Frontend Status
- Modern SaaS web application built with Next.js 16 (React 19, Tailwind CSS v4, Lucide icons, Geist fonts):
  - `frontend/lib/api.ts`: Typed API client for auth, resume upload, profile preview, interview execution, and reports.
  - `frontend/lib/auth-context.tsx`: Client-side JWT session state with localStorage persistence.
  - `frontend/components/Navbar.tsx`: Sticky navbar with brand, theme toggle, user status, and action buttons.
  - `frontend/components/AuthModal.tsx`: Modal for Sign In, Account Creation, and instant Demo login.
  - `frontend/components/PreparationSetupModal.tsx`: 4-step wizard for resume upload, target company/JD, stage/nature calibration, and live InterviewProfile preview.
  - `frontend/components/DashboardView.tsx`: Preparation cockpit with metrics, quick-launch target company presets, and preparation history cards.
  - `frontend/components/InterviewSessionView.tsx`: Real-time mock interview environment with live message stream, monospace code mode, expected focus hints, and keyboard shortcuts.
  - `frontend/components/PreparationReportView.tsx`: Evidence-grounded preparation report with readiness gauge, tier badge, strengths/gaps breakdown, action plan, and provenance citations.

## Testing & Verification
- Backend tests: 15/15 passing (`uv run pytest` in 25.46s), including `test_candidate_api_flow.py` verifying full auth, profile preview, interview execution, and ownership isolation.
- Frontend lint: `npm run lint` passes with 0 errors and 0 warnings.
- Frontend build: `npm run build` compiles with 0 errors, full TypeScript type safety, and static page generation.
