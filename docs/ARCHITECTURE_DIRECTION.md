# Architecture Direction

## Purpose
This document describes the target architecture at a conceptual level for the new candidate-first interview preparation product. It intentionally avoids locking in final implementation details for storage, search, or web research.

## Frontend / backend boundary
The frontend should be the candidate-facing preparation application. The backend remains the core orchestration and service layer.

Clear responsibilities:
- Frontend responsibilities:
  - candidate auth and session
  - resume/JD/company intake
  - interview session UI
  - answer capture
  - report display
  - interview history
- Backend responsibilities:
  - candidate profile generation
  - Interview Profile construction
  - orchestration of candidate prep workflow
  - retrieval and knowledge integration
  - custom evaluation logic
  - report generation and provenance
  - persistence and authorization

The current frontend is a scaffold and should not be treated as a complete product boundary. The backend should remain the more mature component for the pivot.

## Authentication
Authentication should continue to provide secure candidate identity and access control.

Required responsibilities:
- candidate sign-up/login
- protected interview and report access
- role-aware access control
- server-side enforcement of candidate ownership
- session security consistent with the existing backend assumptions

Existing JWT-based auth should likely be preserved unless there is evidence of a stronger requirement for a different model.

## Candidate profile
The candidate profile should remain a first-class concept but must expand beyond a resume-only profile.

The profile should capture:
- candidate background
- skills and competencies
- experience and strengths
- target role, company, and JD context
- interview preparation history

This should coexist with the Interview Profile, which is more task- and interview-specific than the base candidate record.

## Interview / session model
The interview/session model should be oriented around candidate preparation rather than recruiter operations.

The model should track:
- candidate identity
- Interview Profile
- current question and answer state
- follow-up status
- evaluation state
- report state
- session lifecycle and completion

This is conceptually aligned with the existing interview state model and LangGraph flow, but the business semantics should shift from hiring management to candidate prep.

## Interview Profile
Interview Profile is the central domain concept for the pivot.

It acts as the configuration object for a preparation run and should unify:
- company
- role
- stage
- nature
- focus areas
- question style
- difficulty
- question/follow-up count
- supporting evidence

This is the canonical object that links the candidate, the target opportunity, and the interview generation logic.

## Interview orchestration / LangGraph
The existing LangGraph flow is a strong architectural base and should likely be preserved where practical.

The orchestration responsibilities should remain:
- answer processing
- follow-up decisioning
- evaluation of responses
- progression through the session
- report generation

The workflow should be re-centered around candidate prep, but the orchestration pattern itself is still valuable and likely reusable.

## Retrieval layer
The existing retrieval architecture is a meaningful foundation for the new direction.

The retrieval layer should support multiple context sources:
- internal technical knowledge
- reusable company knowledge
- candidate-specific context
- live research sources when required

The retrieval architecture should be designed to be multi-source rather than single-source technical retrieval.

Implementation decisions are intentionally deferred, but the architectural responsibility is clear: retrieval should combine relevant knowledge sources into an interview-ready context bundle.

## Internal technical knowledge
Internal technical knowledge should remain a reusable source of domain fundamentals, role-specific concepts, and frameworks.

This likely corresponds to the repository’s existing RAG and retrieval concepts and should be preserved where it still aligns with the product.

## Company knowledge
Company knowledge becomes a first-class domain concept.

It should cover:
- company business model and context
- product area or business domain
- likely interview themes
- role-specific company expectations
- durable interview-prep context

This should be modular from the technical-knowledge system, because company knowledge is not the same as general domain retrieval.

## Live research
Live web research is a major product requirement for new or stale companies.

Architecturally, this should be treated as a distinct responsibility layer that may:
- fetch fresh company information
- extract relevant interview-relevant facts
- produce a temporary or persisted company knowledge update
- enrich the reusable company knowledge store

This does not require choosing the final implementation yet, but it does require a boundary between “reusable company memory” and “fresh web-derived context.”

## Evidence / provenance
Evidence and provenance are now a required part of the product.

The architecture should preserve the origin of recommendations and evaluations:
- candidate-provided inputs
- internal technical knowledge
- company memory
- live research findings
- answer-level evidence

This should be represented as a structured provenance layer or metadata schema, even if the exact storage mechanism is deferred.

## Evaluation
Evaluation should become stage- and nature-aware, not a single fixed rubric.

The evaluation boundary should be responsible for:
- picking a stage-appropriate rubric
- using the Interview Profile and context
- scoring answer quality, relevant reasoning, and completeness
- generating evidence-based improvement guidance

The existing evaluation services are likely valuable as a foundation but will need to be adapted to contextual evaluation logic.

## Reporting
The reporting layer should shift from recruiter-facing hiring output to a candidate-first preparation report.

The report should combine:
- readiness signal
- strengths and gaps
- evidence summary
- company/role focus areas
- next-step preparation guidance

This is closer to a prep report than a hiring recommendation report.

## Persistence
Persistence should be extended to accommodate the new product concepts.

Likely persisted entities include:
- candidate
- resume/JD/company context
- Interview Profile
- interview session state
- answer records
- evaluation records
- prep report
- company knowledge entries
- research provenance records

The existing MongoDB-based persistence and interview schema are likely useful foundations, but the data model must expand to support the new product semantics.

## Existing components likely to be preserved
The following are likely valuable to keep and adapt:
- existing FastAPI backend structure
- JWT-related auth flow
- CandidateProfile concepts and candidate data model
- interview planning and query-planning concepts
- interview state session model and LangGraph orchestration
- hybrid retrieval engine concepts
- evaluation/reporting service patterns
- MongoDB persistence model as a base layer

## Existing components likely to be refactored or re-scoped
The following are likely to need significant re-scoping:
- recruiter/interviewer workflows and derived API assumptions
- recruiter report semantics and data model
- interview creation and dashboard assumptions centered on interviewer operations
- any product assumptions that treat the candidate as a passive interview subject rather than the primary prep user
- evaluation/reporting output formatting toward hiring decisions rather than preparation guidance

## Recruiter-specific components likely candidates for removal or transformation
- interviewer dashboards
- recruiter/analytics-first reporting
- interviewer ownership and assignment semantics as primary user modeling
- recruiter-driven candidate lists and review flows
- hiring recommendation outputs as core business value

These should not be deleted blindly without product scope decisions, but they are the clearest legacy areas to reframe or remove.
