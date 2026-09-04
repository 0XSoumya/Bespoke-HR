# AGENTS.md

## Project

This repository contains an Adaptive AI Interview System.

The system conducts personalized technical interviews using resume intelligence, retrieval-augmented generation, adaptive follow-up questioning, automated evaluation, and candidate/recruiter reporting.

This is a portfolio project, but implementation quality must demonstrate production-grade SaaS engineering practices.

## Mission

Audit, improve, and complete the existing application without unnecessarily replacing working functionality.

Preserve existing interview, RAG, evaluation, reporting, persistence, and API behavior unless a change is required for correctness, security, maintainability, or an explicit product requirement.

Do not rewrite working systems merely to use a different technology.

## Required Reading

Before making substantial changes, inspect:

1. PROJECT_SPEC.md
2. README.md
3. Relevant source code
4. Relevant tests
5. Relevant configuration
6. Existing Git history

The repository is the source of truth for existing behavior.

PROJECT_SPEC.md defines product and engineering requirements.

## Decision Priority

When requirements conflict, use this order:

1. Explicit user requirements
2. PROJECT_SPEC.md
3. AGENTS.md
4. Existing working behavior
5. Installed design and engineering skills
6. Framework and library conventions
7. Implementation preference

When a requirement is not specified, make the simplest professional decision that fits the existing architecture.

Do not ask for confirmation for routine implementation decisions.

Ask the user only when genuinely blocked by:

- missing credentials
- external authorization
- destructive operations
- an ambiguity that cannot reasonably be resolved from the repository or specification

## Existing Functionality

Do not regress:

- resume upload and parsing
- candidate profile generation
- retrieval and RAG
- interview planning
- LangGraph interview workflow
- main-question generation
- adaptive follow-up generation
- follow-up limits
- answer evaluation
- interview persistence
- recruiter reporting
- candidate reporting
- existing API behavior unless intentionally versioned or improved

Existing bugs may be fixed when discovered.

## Backend

Use the existing FastAPI architecture unless a strong reason exists to refactor it.

Apply:

- API versioning
- Pydantic validation
- consistent error responses
- clear service boundaries
- repository/data-access separation where useful
- structured logging
- environment-based configuration
- appropriate exception handling
- type hints
- secure defaults
- testable service logic

Do not expose secrets.

Never hard-code:

- API keys
- database credentials
- JWT secrets
- passwords
- tokens
- other sensitive values

## Security

Treat authentication and authorization as separate concerns.

Implement or improve:

- authentication
- secure password hashing
- token/session security
- role-based access control
- object-level authorization
- input validation
- upload validation
- upload size limits
- secure CORS configuration
- secure HTTP behavior where appropriate
- rate limiting where appropriate
- safe error responses
- safe logging
- privacy protections
- appropriate audit logging
- secret management

A user must never gain access to another user's interview, report, candidate data, or interviewer functionality by changing an ID in a request.

Authorization must be enforced server-side.

## Frontend

Build a polished, responsive SaaS web application.

The frontend should feel intentionally designed and professionally built rather than generated from a generic AI template.

Use:

- shadcn/ui as the component foundation where appropriate
- the installed Taste Skill for visual direction
- Vercel Web Interface Guidelines for accessibility, interaction, UX, and frontend quality
- React Bits selectively when an individual component materially improves the experience

Do not use a library merely because it is available.

Avoid:

- generic AI landing-page aesthetics
- excessive glassmorphism
- excessive gradients
- meaningless animations
- generic three-column card grids
- giant headings without hierarchy
- generic placeholder marketing copy
- arbitrary decorative elements
- inaccessible interactions

Animations must support hierarchy, feedback, navigation, or atmosphere.

Respect prefers-reduced-motion.

The application must work well on desktop, tablet, and mobile.

## Skills

The project has the following installed agent skills:

- design-taste-frontend
- web-design-guidelines

Use them where relevant.

### Taste Skill

Use Taste for:

- visual direction
- composition
- hierarchy
- typography
- density
- visual polish
- motion language
- avoiding generic design patterns

### Vercel Web Interface Guidelines

Use the Web Interface Guidelines for:

- accessibility
- interaction quality
- forms
- keyboard behavior
- focus states
- responsive behavior
- errors
- usability
- frontend implementation quality

Do not allow the skills to override explicit project requirements.

## Component and Animation Libraries

Use shadcn/ui as the primary UI component foundation where appropriate.

React Bits may be used selectively.

Do not install or copy the entire React Bits collection.

Prefer CSS transitions and existing project capabilities for simple animation.

Add Anime.js only if it provides a clear benefit over simpler implementation.

ApexCharts may be added if it is the best fit for recruiter analytics.

Do not add dependencies merely for novelty.

## Assets

Do not block implementation on external imagery.

Prefer project-native visuals such as:

- typography
- CSS
- SVG
- gradients
- geometric elements
- icons
- charts
- data visualization
- animation
- UI composition

If external imagery would materially improve the design:

1. Use a deliberate local placeholder.
2. Document the requirement in docs/ASSETS.md.
3. Continue implementation.
4. Defer final asset replacement to Phase 2.

Do not use random stock imagery merely to fill space.

Do not use AI-generated imagery.

Any external asset eventually added to the public repository must have an appropriate license.

## Documentation

Document meaningful architectural decisions.

Create or update documentation when implementation changes:

- architecture
- API contracts
- authentication
- authorization
- RAG
- retrieval
- evaluation
- data models
- testing
- security
- deployment
- debugging
- frontend architecture

Use clear technical English.

Prefer short sentences and concrete terminology.

Use ASD-STE100-inspired technical writing principles where practical.

Documentation must describe the actual implementation.

Do not create documentation that merely repeats obvious source code.

## Testing

Before considering work complete:

- run backend tests
- run frontend linting
- run frontend production build
- run relevant API tests
- test authentication
- test authorization
- test important failure paths
- test resume upload
- test the interview flow
- test follow-up behavior
- test report generation
- test responsive behavior where practical
- run the Vercel Web Interface Guidelines review

Fix discovered issues when they are within scope.

Do not merely report problems that can reasonably be fixed.

## Git

Use Git actively.

Before changes:

- inspect git status
- inspect recent commits
- understand the current branch

Create coherent commits for meaningful milestones.

Use conventional commit prefixes where appropriate:

- feat:
- fix:
- refactor:
- test:
- docs:
- security:
- perf:
- chore:

Never:

- commit secrets
- commit .env
- force-push
- rewrite existing history
- delete unrelated user work
- perform destructive resets

Do not push to a remote unless explicitly requested.

## Working Style

Work autonomously.

First inspect and understand the repository.

Then form an implementation plan.

Then implement the plan end-to-end.

Do not stop after identifying problems.

Do not leave TODO comments instead of implementing required functionality.

Do not create fake implementations merely to make tests pass.

Prefer small, reversible changes over unnecessary rewrites.

### Backend authority

Be conservative with the existing backend architecture.

Preserve working functionality.

Refactor when required for:

- correctness
- security
- maintainability
- testability
- explicit product requirements

### Frontend authority

The existing frontend is an implementation starting point, not a visual constraint.

Preserve required functionality, but substantial frontend restructuring or replacement is allowed when necessary to create the product described in PROJECT_SPEC.md.

Do not make superficial CSS changes when a proper redesign is warranted.

## Completion

At the end:

1. Verify the important user flows.
2. Run the relevant tests.
3. Run frontend lint and build.
4. Review security.
5. Review accessibility.
6. Review responsive behavior.
7. Review documentation.
8. Inspect Git status.
9. Create coherent commits.
10. Provide a concise final report.

The final report must include:

- what was implemented
- important architectural changes
- tests performed
- security improvements
- frontend/design improvements
- documentation created or updated
- remaining limitations
- Git commits created