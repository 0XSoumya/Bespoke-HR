# Target Product Specification

## Product purpose
Bespoke is a candidate-first AI interview preparation platform. The product helps candidates prepare for a specific company, role, and interview round by combining their resume, the job description, company context, stage-aware interview expectations, and adaptive assessment.

The platform is intended to help candidates improve readiness before interviews rather than to support recruiter screening workflows.

## Primary user
- Primary user: candidate preparing for a specific interview.
- Secondary users: optionally, a returning candidate managing preparation history and prior reports.
- Recruiter/interviewer workflows are not the primary product and are not required for the first production release.

## Core user journey
1. Candidate provides resume, company, target role, and job description.
2. Candidate selects interview stage and interview nature.
3. Candidate configures interview size (primary questions and follow-ups).
4. System analyzes the candidate and the JD.
5. System assembles or enriches company-specific context.
6. System constructs an Interview Profile.
7. System generates an adaptive interview tailored to the candidate and the target role/company.
8. Candidate answers questions.
9. System evaluates answers using a stage- and nature-appropriate rubric.
10. System produces an evidence-grounded preparation report.

## Interview configuration
The candidate supplies the following inputs:
- resume
- company
- target role
- job description
- interview stage
- interview nature/type
- desired number of primary questions
- desired number of follow-ups

These inputs should be treated as explicit product requirements rather than optional metadata.

## Interview Profile
Interview Profile is a central domain concept.

At minimum, it should represent:
- company
- role
- interview stage
- interview nature
- focus areas
- question style
- difficulty
- duration/question configuration
- supporting evidence

Stage and nature are distinct concepts and must not be collapsed into a single field.

Examples of stage/nature values (not final taxonomy):
- Technical Round 1
- Technical Round 2
- Coding Screen
- ML/AI Deep Dive
- System Design
- Behavioral/HR
- Hiring Manager
- Final Round
- Custom/Mixed

The final taxonomy is intentionally deferred.

## Company-specific preparation
Company-specific interviewing is a core feature of the new product.

The system should combine:
- the candidate’s resume and background
- the role and job description
- internal technical knowledge
- company-specific knowledge
- live research when needed

Company-specific preparation is not optional; it is a core differentiator.

## Adaptive interview
The system must generate a tailored adaptive interview that responds to:
- candidate strengths and gaps
- target role requirements
- job description emphasis
- company context
- interview stage and nature
- prior answers and follow-ups

The interview is expected to be dynamic, not static. Candidate answers should influence future questions and follow-up depth.

## Evaluation
Answers must be evaluated using a rubric appropriate to the candidate’s interview stage and the interview nature.

Examples of evaluation adaptation:
- coding screen emphasizes correctness, tradeoffs, and process
- system design emphasizes scalability, choices, and communication
- behavioral/HR emphasizes clarity, examples, and motivation
- AI/ML deep dive emphasizes model tradeoffs, evaluation, and operational understanding

The rubric should be contextual and evidence-aware rather than a single universal score.

## Preparation report
The final report should be written as a preparation artifact, not a hiring decision artifact.

It should include:
- readiness summary
- strengths
- gaps
- likely question themes
- role/company focus areas
- evidence for recommendations
- suggested follow-up preparation actions

The report should be grounded in candidate evidence, retrieved context, and review of answers, not simply a general score.

## Evidence / provenance expectations
Evidence is a required product concept.

The system should distinguish between:
- internal technical knowledge
- company-specific knowledge
- live research findings
- candidate-provided resume/JD context
- answer-specific evidence

The product should preserve enough provenance to explain why a recommendation or evaluation was made.

This is not a final implementation commitment, but it is a confirmed product requirement of the candidate-first direction.

## Authentication and account model
The application must support candidate authentication and account management.

Confirmed requirements:
- candidate login / signup flow
- protected interview and report access
- server-side authorization
- candidate should only access their own interview and preparation data

The recruiter/interviewer account model is not the primary product path and may be reduced or removed for the first release.

## Interview history
The system should support a candidate’s preparation history, including:
- prior interviews
- stage-specific preparation sessions
- performance summaries
- past reports and recommendations

This should be treated as part of the candidate prep experience but not necessarily as a recruiter workflow.

## Explicit non-goals for the first production release
The following are intentionally out of scope for the first production release:
- finalizing a universal company knowledge taxonomy
- finalizing the exact vector-store architecture
- finalizing the exact live-research implementation
- finalizing a strict company knowledge freshness policy
- finalizing a definitive stage taxonomy
- full recruiter dashboard or hiring workflow
- full multi-role admin or interviewer orchestration
- mandatory web search for every company and every interview

## Confirmed requirements
- candidate-first product orientation
- resume + JD + company + interview context intake
- Interview Profile as a central concept
- company-specific interview preparation as a core workflow
- adaptive interview generation
- interview-stage and nature-specific evaluation
- evidence-grounded preparation report
- hybrid internal knowledge + company knowledge + live research direction
- preserving valuable existing backend interview/RAG/evaluation functionality where practical

## Intentionally deferred decisions
- final company knowledge storage model
- exact internal company knowledge vs live web research policy
- exact freshness strategy
- source validation and trust rules
- final stage taxonomy
- exact report evidence standard
- final vector-store/search architecture
