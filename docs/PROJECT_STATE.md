# Project State Snapshot

## Repository status
- Git HEAD: `cbf764a`
- Graphify graph status: likely current for the backend code graph, but not a definitive product-level truth source. The repo contains a generated graph under `graphify-out/` and a report under `graphify-out/GRAPH_REPORT.md`; it should be treated as a code-structure snapshot, not as a final product-state source.

## Backend status
- Substantial backend functionality already exists and is the strongest implemented area.
- Present functionality includes:
  - JWT authentication and role-aware access primitives
  - resume parsing and candidate profile creation
  - interview planning and query-planning logic
  - hybrid retrieval stack (semantic + keyword)
  - FAISS/Voyage/BM25 retrieval components
  - LangGraph interview execution
  - follow-up generation
  - answer evaluation
  - report generation
  - MongoDB persistence
- Major backend files include:
  - `backend/app/main.py`
  - `backend/app/api/routes/auth.py`
  - `backend/app/api/routes/resume.py`
  - `backend/app/api/routes/interview.py`
  - `backend/app/services/interview/*`
  - `backend/app/services/retrieval/*`
  - `backend/app/services/resume/*`
  - `backend/app/graph/interview_graph.py`

## Frontend status
- Frontend is currently a Next.js scaffold and is not wired to the backend.
- It does not yet implement the candidate-first product flow.
- Current signs of incompleteness include the default landing page in `frontend/app/page.tsx` and default root metadata in `frontend/app/layout.tsx`.

## AI pipeline status
- The backend AI pipeline is materially present and connected internally:
  - resume intake -> candidate profile
  - interview planning -> query planning -> retrieval
  - question generation -> interview execution
  - follow-up -> evaluation -> report generation
- The pipeline is still oriented toward a general adaptive interview product and not yet centered on candidate prep + company-specific interviewing.

## Persistence status
- MongoDB persistence is already in place and used by the interview and candidate flows.
- Persistence is generally present for interview state, candidate records, and user accounts.
- The repository still contains both app-level repository modules and database-specific modules, indicating some partial migration or duplication.

## Authentication status
- JWT-based authentication exists and is structurally in place.
- Role-aware access and auth routing exist.
- The application still contains recruiter/interviewer-oriented concepts that need to be reframed for the candidate-first product.

## Testing status
- Test coverage exists for multiple backend areas, including interview, retrieval, follow-up, persistence, and reporting.
- The tests are backend-centric and do not yet cover the full candidate-first product flow or the frontend.

## Deployment status
- A Dockerfile and basic deployment scaffolding exist.
- There is no evidence of a completed production deployment setup for the new product direction.

## Known technical debt
- Recruiter/interviewer-oriented product assumptions remain in code and docs.
- Frontend is not connected to backend product flows.
- Some persistence and repository layering may be duplicated or transitional.
- Product requirements and architecture still reflect the older recruiter-centric model in several documents.
- Company-specific knowledge and live web research are not yet formalized as first-class product concepts.

## Known broken or partial areas
- Frontend product implementation is effectively unconnected to the backend product experience.
- Product requirements still contain recruiter-oriented flows and artifacts.
- Company-specific preparation and source provenance are not yet formalized as system requirements.
- Company research and knowledge freshness policy are intentionally unresolved, which means the architecture is not yet complete for the new direction.

## Recruiter-specific legacy areas
- Recruiter reporting, interviewer dashboards, analytics workflows, and interviewer-created interview flows are legacy product assumptions.
- These concepts remain in the repository and should be reduced or transformed rather than treated as primary product requirements.

## Immediate next milestone
- Establish the new product baseline: candidate-first onboarding, Interview Profile, company/JD intake, and stage/nature-aware planning, while preserving the valuable existing backend interview/RAG/evaluation foundation.
