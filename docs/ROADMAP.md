# Roadmap

## Phase 1: Product-pivot architecture and data-model cleanup
Objective:
- Align the existing codebase with the new candidate-first product direction before adding new behavior.

Major deliverable:
- Updated domain model and product vocabulary for candidate prep, Interview Profile, company context, and evidence/provenance.

Dependencies:
- This phase should start before new user-flow work.

Acceptance criteria:
- the repository has a clear distinction between candidate profile, Interview Profile, and interview/session state
- recruiter-specific concepts are explicitly flagged for removal or transformation
- the product can be described without the old recruiter-centric narrative

Likely files/modules affected:
- `PROJECT_SPEC.md` and `README.md` (already docs-driven governance)
- `backend/app/models/schemas/*`
- `backend/app/services/interview/*`
- `backend/app/api/routes/*`

## Phase 2: Authentication and candidate access
Objective:
- Ensure candidate-first access control and secure session behavior are in place.

Major deliverable:
- candidate auth, protected interview access, and user-owned prep history.

Dependencies:
- Phase 1 domain model

Acceptance criteria:
- candidate can sign in and access only their own data
- protected endpoints enforce ownership
- recruiter-only assumptions are no longer core to the system

Likely files/modules affected:
- `backend/app/core/security.py`
- `backend/app/api/deps.py`
- `backend/app/api/routes/auth.py`
- `backend/app/repositories/user_repository.py`

## Phase 3: Candidate onboarding and intake
Objective:
- Support the candidate’s real initial product flow: resume, company, role, JD, and interview settings.

Major deliverable:
- candidate intake and prep request creation from a single product flow.

Dependencies:
- Phase 1 domain model
- Phase 2 auth

Acceptance criteria:
- candidate can submit resume + JD + company + role + stage + nature + question configuration
- intake information is persisted and associated with the correct candidate
- the system can generate a prep session from that data

Likely files/modules affected:
- `backend/app/api/routes/resume.py`
- `backend/app/services/resume/*`
- `backend/app/repositories/candidate_repository.py`
- relevant schema files in `backend/app/models/schemas/`

## Phase 4: Interview Profile creation
Objective:
- Produce a canonical Interview Profile as the center of the preparation workflow.

Major deliverable:
- Interview Profile object with company, role, stage, nature, focus areas, style, difficulty, duration, and supporting evidence.

Dependencies:
- Phase 3 intake

Acceptance criteria:
- Interview Profile is generated from candidate and JD data
- stage and nature are explicitly separate values
- supporting evidence is associated with the profile

Likely files/modules affected:
- `backend/app/models/schemas/*`
- `backend/app/services/interview/interview_planner_service.py`
- `backend/app/services/interview/role_config.py`

## Phase 5: Interview creation and planning
Objective:
- Turn the Interview Profile into a plan for a tailored interview.

Major deliverable:
- Interview plan, query plan, and retrieval inputs for the candidate preparation flow.

Dependencies:
- Phase 4 Interview Profile
- existing retrieval flow

Acceptance criteria:
- the system can transform a candidate and company-specific profile into a targeted interview plan
- question count and follow-up counts are respected
- focus areas and difficulty are consistent with the stage and nature

Likely files/modules affected:
- `backend/app/services/interview/interview_engine.py`
- `backend/app/services/interview/interview_planner_service.py`
- `backend/app/services/interview/query_planner_service.py`
- `backend/app/services/interview/retrieval_orchestrator.py`

## Phase 6: End-to-end interview UI
Objective:
- Deliver the candidate-facing interview experience in the frontend.

Major deliverable:
- a working candidate interview UX that is wired to the backend product flow

Dependencies:
- Phases 2-5

Acceptance criteria:
- candidate can start a prep interview
- answer submission works end-to-end
- current question and progress state are visible
- follow-up flow works from the frontend

Likely files/modules affected:
- `frontend/app/*`
- `frontend/components/*`
- backend interview routes and state APIs

## Phase 7: Adaptive follow-ups and answer progression
Objective:
- Make the interview adaptive and stage-aware.

Major deliverable:
- follow-up generation and state progression driven by the Interview Profile and answer quality.

Dependencies:
- Phase 5 interview planning
- Phase 6 UI

Acceptance criteria:
- follow-ups are generated according to candidate answers and context
- follow-up count limits are enforced
- stage and nature influence follow-up behavior

Likely files/modules affected:
- `backend/app/graph/interview_graph.py`
- `backend/app/services/interview/followup_service.py`
- `backend/app/services/interview/session_service.py`

## Phase 8: Evaluation and scoring adjustments
Objective:
- Replace generic evaluation assumptions with stage- and nature-aware evaluation.

Major deliverable:
- evaluation rubric tied to stage/nature and Interview Profile.

Dependencies:
- Phase 4 Interview Profile
- Phase 7 follow-up flow

Acceptance criteria:
- evaluation outputs differ meaningfully by stage/nature
- answer quality is mapped to interview goals and company context
- evaluation evidence is captured for the final report

Likely files/modules affected:
- `backend/app/services/interview/evaluation_service.py`
- `backend/app/models/schemas/question_evaluation.py`
- `backend/app/services/interview/evaluation_prompt.py`

## Phase 9: Preparation report
Objective:
- Generate an evidence-grounded, candidate-focused preparation report.

Major deliverable:
- final prep report that summarizes readiness, strengths, gaps, and next best preparation steps.

Dependencies:
- Phase 8 evaluation

Acceptance criteria:
- report is oriented toward preparation, not hiring recommendation
- report includes evidence and provenance
- report is understandable to the candidate without recruiter workflows

Likely files/modules affected:
- `backend/app/services/interview/report_service.py`
- `backend/app/models/schemas/interview_report.py`
- `backend/app/api/routes/interview.py`

## Phase 10: Company-specific research and knowledge enrichment
Objective:
- Add the new company-specific knowledge pillar without locking the final implementation.

Major deliverable:
- a company-knowledge pipeline that supports reusable memory and live research fallback.

Dependencies:
- Phase 4 Interview Profile
- Phase 9 report generation

Acceptance criteria:
- company context can be assembled from reusable knowledge and fresh research when needed
- research findings are provenance-tagged
- stale or missing company knowledge triggers enrichment rather than blind reliance

Likely files/modules affected:
- new domain services, retrieval modules, and storage abstractions
- company-related models and evaluation/reporting attachments

## Phase 11: Production hardening
Objective:
- Make the candidate-first system ready for reliable operation.

Major deliverable:
- production-safe config, security, logging, resilience, and deployment readiness.

Dependencies:
- all prior phases

Acceptance criteria:
- secure auth and ownership enforcement are complete
- logs and monitoring are structured and useful
- secrets and environment requirements are documented
- deployment path is coherent for candidate-facing service

Likely files/modules affected:
- `backend/app/main.py`
- `backend/app/core/config/settings.py`
- `backend/app/core/security.py`
- deployment and environment docs

## Phase 12: Testing, observability, and deployment
Objective:
- Reduce risk before launch and validate the real product flows.

Major deliverable:
- regression protection for core product behaviors and deployment readiness.

Dependencies:
- earlier phases and hardening

Acceptance criteria:
- end-to-end candidate prep flows are tested
- frontend/backend integration is tested
- observability and metrics exist
- deployment is documented and repeatable

Likely files/modules affected:
- `backend/tests/*`
- frontend testing and integration layers
- deployment configuration
