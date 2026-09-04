# Adaptive AI Interview System — Project Specification

## 1. Product

The Adaptive AI Interview System is a web application that conducts personalized technical interviews.

The system uses:

- candidate resume information
- role requirements
- retrieval-augmented generation
- adaptive questioning
- follow-up questions
- automated answer evaluation
- recruiter reporting
- candidate reporting

The goal is to demonstrate a complete AI product rather than an isolated LLM feature.

This is a portfolio project. Implementation quality should demonstrate SaaS-grade engineering.

## 2. Users

The application has two primary roles.

### Interviewer

The interviewer can:

- create interviews
- configure interview parameters
- select the candidate
- select the target role
- configure the number of main questions
- view interview status
- review completed interviews
- view recruiter reports
- view useful interview analytics

### Candidate

The candidate can:

- create an account
- authenticate
- view scheduled interviews
- enter an available interview
- complete the interview
- submit answers
- receive adaptive follow-up questions
- view or download the candidate report when available

## 3. Main Product Flow

The main product flow is:

Landing Page
    |
    v
Authentication
    |
    v
Role-aware application
    |
    +-- Interviewer
    |      |
    |      +-- Dashboard
    |      +-- Create Interview
    |      +-- Manage Interviews
    |      +-- Candidate Results
    |      +-- Reports
    |      +-- Analytics
    |
    +-- Candidate
           |
           +-- Dashboard
           +-- Scheduled Interviews
           +-- Interview Experience
           +-- Reports

## 4. Interview Flow

The existing interview flow must remain functional.

The system should:

1. receive candidate information
2. process the resume
3. construct a candidate profile
4. identify relevant skills and topics
5. retrieve relevant knowledge
6. plan interview topics
7. generate main questions
8. present a question
9. receive the candidate answer
10. evaluate the answer
11. decide whether a follow-up is useful
12. generate a follow-up when appropriate
13. respect the existing follow-up limit
14. continue through the configured number of main questions
15. generate the final report

The adaptive behavior must not be removed.

## 5. Existing AI Architecture

The current architecture uses:

- Python
- FastAPI
- LangGraph
- Groq
- retrieval-augmented generation
- FAISS
- Voyage embeddings
- hybrid retrieval
- MongoDB

The current Groq model configuration has been migrated from the deprecated Llama 3.3 70B model to:

openai/gpt-oss-120b

Preserve this configuration unless a later requirement explicitly changes it.

## 6. Retrieval

Retain the existing retrieval architecture unless an audit identifies a strong reason to change it.

The first retrieval evaluation revision should implement:

- Recall@K
- Precision@K
- Hit Rate
- MRR
- NDCG@K
- retrieval latency

A reranker experiment is deferred to a later revision.

DeepEval integration is deferred to a later revision.

Do not introduce a reranker or DeepEval merely because they are common technologies.

## 7. Authentication and Authorization

Authentication and authorization are required.

The implementation must support role-aware access.

Authorization must be enforced server-side.

Examples:

- candidates cannot access another candidate's interview
- candidates cannot access interviewer-only functionality
- interviewers cannot access unrelated private resources
- report access must be authorized
- resource IDs must not act as authorization

## 8. API

The backend should use a versioned API.

Prefer a structure such as:

/api/v1/...

Adapt the exact routing structure to the existing application.

API responses and errors should be consistent.

Validation must occur at API boundaries.

Existing endpoints should not be broken unnecessarily.

If an endpoint changes, document the change.

## 9. Frontend

The application should contain:

### Public

- landing page
- product explanation
- clear calls to action
- authentication entry points
- responsive navigation
- metadata
- custom 404
- loading states
- empty states
- error states

### Interviewer

- dashboard
- interview creation
- configurable question count
- interview status
- candidate information
- completed reports
- useful statistics
- analytics

### Candidate

- dashboard
- scheduled interviews
- interview entry
- interview interface
- progress
- answer submission
- report access

## 10. Design

The frontend should feel like a carefully designed modern SaaS product.

It must not resemble a generic AI-generated template.

The exact visual language is intentionally not predetermined.

The design system should be developed using the product requirements and the installed Taste Skill.

The implementation may use:

- typography
- custom layout
- subtle gradients
- SVG
- geometric visual elements
- charts
- tasteful animation
- carefully selected React Bits components
- other appropriate UI techniques

The following are implementation decisions:

- color palette
- typography pairing
- spacing scale
- border radius
- shadows
- component composition
- animation language
- decorative system

They must form a coherent system rather than a collection of unrelated choices.

## 11. Design Quality

Avoid:

- generic AI SaaS templates
- excessive glassmorphism
- excessive gradients
- excessive animation
- decorative elements without purpose
- generic stock photography
- generic filler copy
- repetitive card layouts
- inaccessible interactions

Visual polish should come from hierarchy, composition, typography, spacing, motion, and meaningful visual elements.

## 12. Images and External Assets

External photography is not required for Phase 1.

Prefer native visual design.

If an external image materially improves the final design:

1. use a local placeholder
2. document the asset in docs/ASSETS.md
3. specify the required aspect ratio and visual direction
4. continue implementation
5. defer final asset selection to Phase 2

Do not use AI-generated imagery.

Static appropriately licensed assets may be added later.

## 13. Responsive Design

The application is a responsive web application.

Offline mode and PWA functionality are not requirements.

Support:

- desktop
- tablet
- mobile

Do not add offline infrastructure unless explicitly required later.

## 14. Accessibility

Accessibility is a product requirement.

Follow the Vercel Web Interface Guidelines and established accessibility practices.

Requirements include:

- keyboard navigation
- visible focus
- semantic HTML
- appropriate labels
- accessible forms
- useful validation messages
- accessible dialogs
- appropriate ARIA usage
- reduced-motion support
- sufficient contrast
- mobile-friendly interaction targets

## 15. Security

Security is part of Phase 1.

Address:

- authentication
- password security
- token/session security
- RBAC
- object-level authorization
- input validation
- file validation
- file size limits
- CORS
- secure headers where appropriate
- rate limiting where appropriate
- safe logging
- secret management
- privacy
- data retention
- account deletion considerations

## 16. Testing

### Backend

Test:

- core services
- API validation
- authentication
- authorization
- retrieval
- follow-up behavior
- evaluation
- reporting
- failure paths

### Frontend

Verify:

- lint
- production build
- authentication
- dashboards
- interview experience
- reports
- loading states
- empty states
- error states
- responsive behavior

### End-to-End

Verify the important flow:

Resume
  |
  v
Candidate Profile
  |
  v
Interview Creation
  |
  v
Interview
  |
  v
Main Question
  |
  v
Answer
  |
  v
Follow-up
  |
  v
Next Question
  |
  v
Completion
  |
  v
Evaluation
  |
  v
Report

## 17. Documentation

The project should contain documentation for:

- architecture
- backend
- frontend
- AI pipeline
- retrieval
- data model
- authentication
- security
- testing
- evaluation
- debugging
- deployment
- important architectural decisions

External documentation should help a technical reviewer understand the project.

Internal documentation should help a developer understand and maintain the system.

Documentation must reflect the actual implementation.

## 18. Engineering Freedom

The following are intentionally open:

- exact visual style
- color palette
- typography
- dashboard layout
- component composition
- animation implementation
- frontend state-management approach
- API module organization
- repository/data-access structure
- chart library
- external asset selection

Make professional decisions based on the existing repository and this specification.

Do not introduce technology solely for novelty.

## 19. Phase 1 Definition of Done

Phase 1 is complete when:

- existing backend functionality works
- existing interview flow works
- authentication is implemented
- authorization is enforced
- API structure is versioned
- backend quality is improved
- retrieval evaluation is implemented
- frontend is redesigned into a cohesive product
- interviewer workflows work
- candidate workflows work
- reports work
- analytics work where appropriate
- loading/error/empty states exist
- accessibility requirements are addressed
- frontend lint/build passes
- backend tests pass
- important end-to-end flows are verified
- documentation is updated
- security issues found during the audit are addressed
- coherent Git commits exist

## 20. Phase 2

Potential Phase 2 work:

- curated external imagery
- retrieval reranking experiments
- DeepEval
- deeper AI evaluation
- additional analytics
- further visual polish
- deployment refinements
- additional product features

Phase 2 must not be used as an excuse to leave Phase 1 functionality incomplete.