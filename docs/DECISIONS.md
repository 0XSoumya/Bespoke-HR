# Decisions

## Established decisions
- **Candidate-First Product Direction**: The application is an AI-powered technical interview preparation system designed for software engineers practicing for high-stakes interviews, not a recruiter screening tool.
- **Canonical InterviewProfile**: The central domain model uniting candidate competencies, job requirements, stage/nature expectations, and company intelligence.
- **Stage & Nature Separation**: Interview stage (e.g., Technical Round 1, System Design, Behavioral, Final Round) and interview nature (e.g., Coding, System Design, ML/AI Technical, Behavioral) are distinct orthogonal dimensions that calibrate questioning style and evaluation rubrics.
- **Multi-Tier Company Intelligence**: Curated memory for Tier-1 companies (Stripe, Google, Meta, Amazon, OpenAI, Anthropic) paired with dynamic fallback research for arbitrary companies, complete with evidence provenance citations.
- **Strict Server-Side Ownership**: Candidate mock interviews and reports are strictly private. Access across candidate boundaries is blocked with HTTP 403 Forbidden; unauthenticated access on owned sessions is blocked with HTTP 401 Unauthorized. Recruiter evaluation reports are hidden from candidates.
- **DatabaseProxy for Async Motor**: Replaced static global Motor client with dynamic event loop-aware proxy in `backend/app/core/database.py` to prevent event loop closure failures under pytest-asyncio and multiple concurrent async loops.
- **Frontend Aesthetic & Architecture**: Modern SaaS interface using Next.js 16 (React 19, Tailwind CSS v4, Lucide icons, Geist typography) following the anti-slop guidelines (Linear/Vercel feel, dark mode default, restrained micro-interactions, responsive on desktop and mobile).
- **Evidence Provenance Standards**: Every evaluation score, company insight, and recommended prep action is backed by an `EvidenceItem` with confidence percentage and source attribution.
