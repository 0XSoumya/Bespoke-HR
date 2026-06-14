# Adaptive AI Interview System

An AI-powered interview platform that conducts personalized technical interviews using Retrieval-Augmented Generation (RAG), adaptive follow-up questioning, and automated candidate evaluation.

The system analyzes a candidate's resume, generates role-specific interview questions, dynamically adapts based on responses, and produces detailed recruiter and candidate reports.

## Architecture

```mermaid
flowchart TD

    A[Resume Upload] --> B[Resume Parser]
    B --> C[Candidate Profile]

    C --> D[Interview Planner]
    D --> E[Query Planner]

    E --> F[Retrieval Engine]
    F --> G[FAISS Vector Store]
    F --> H[Knowledge Base]

    E --> I[Question Generator]

    I --> J[LangGraph Interview Workflow]

    J --> K[Question Presentation]
    J --> L[Followup Generator]
    J --> M[Evaluation Engine]

    M --> N[Question Evaluation]
    N --> O[Report Generator]

    O --> P[Recruiter Report]
    O --> Q[Candidate Report]

    J --> R[(MongoDB)]
```

---

## Overview

Traditional interviews often follow a static question set regardless of a candidate's background, experience, or performance.

This project introduces an intelligent interview workflow that:

* Parses and analyzes resumes
* Builds structured candidate profiles
* Retrieves domain knowledge from a curated knowledge base
* Generates role-specific technical questions
* Produces adaptive follow-up questions
* Evaluates candidate responses
* Generates recruiter and candidate reports

The entire interview lifecycle is orchestrated using LangGraph.

---

## Key Features

### Resume Intelligence

* PDF resume ingestion
* Structured candidate profile extraction
* Skills identification
* Project extraction
* Experience summarization

### Retrieval-Augmented Question Generation

* Knowledge-base-driven interview generation
* Hybrid retrieval architecture
* FAISS vector search
* Query expansion
* Topic-aware retrieval

### Adaptive Interviews

* Dynamic question generation
* Context-aware follow-up questions
* Multi-turn interview flow
* Candidate-specific questioning

### Automated Evaluation

* Conceptual understanding assessment
* Technical depth evaluation
* Completeness scoring
* Communication assessment

### Report Generation

Recruiter Report:

* Overall score
* Topic-wise scores
* Strengths
* Weaknesses
* Hiring recommendation

Candidate Report:

* Performance summary
* Areas for improvement
* Learning recommendations

---

## System Architecture

```text
Resume Upload
      │
      ▼
Resume Parser
      │
      ▼
Candidate Profile
      │
      ▼
Interview Planner
      │
      ▼
Query Planner
      │
      ▼
Retrieval Engine
      │
      ▼
Question Generator
      │
      ▼
LangGraph Interview Workflow
      │
      ├── Follow-up Generation
      ├── Evaluation
      └── State Management
      │
      ▼
Report Generator
```

---

## Tech Stack

### Backend

* Python
* FastAPI
* LangGraph
* Pydantic

### LLM Layer

* Groq API
* LLM-powered:

  * Resume Parsing
  * Question Generation
  * Follow-up Generation
  * Evaluation
  * Reporting

### Retrieval

* FAISS
* Voyage Embeddings
* Hybrid Search
* Query Expansion

### Database

* MongoDB

---

## Project Structure

```text
backend/
│
├── app/
│   ├── api/
│   ├── graph/
│   ├── services/
│   │   ├── interview/
│   │   ├── retrieval/
│   │   ├── resume/
│   │   └── llm/
│   ├── repositories/
│   └── models/
│
├── knowledge_base/
├── scripts/
├── tests/
└── pyproject.toml

frontend/
```

---

## Interview Workflow

### Step 1

Upload Resume

Candidate resume is parsed and converted into a structured profile.

### Step 2

Create Interview

The system:

* Analyzes candidate strengths
* Determines interview focus areas
* Builds an interview plan

### Step 3

Retrieve Context

Relevant knowledge is retrieved from the vector database for each interview topic.

### Step 4

Generate Questions

Role-specific technical questions are generated using retrieval context.

### Step 5

Adaptive Follow-Ups

Based on candidate responses, the system generates targeted follow-up questions.

### Step 6

Evaluate Responses

Each question is evaluated across multiple dimensions:

* Conceptual Accuracy
* Completeness
* Technical Depth
* Communication

### Step 7

Generate Reports

Recruiter and candidate reports are produced automatically.

---

## Example Topics

For a GenAI Engineer role, the system can assess:

* Retrieval-Augmented Generation (RAG)
* Embeddings
* Prompt Engineering
* LLM Evaluation
* Vector Retrieval
* Agentic Workflows
* LangChain
* LangGraph
* Knowledge Retrieval Systems

---

## API Endpoints

### Upload Resume

```http
POST /resume/upload
```

### Create Interview

```http
POST /interviews/create
```

### Submit Answer

```http
POST /interviews/{interview_id}/answer
```

### Get Current Question

```http
GET /interviews/{interview_id}/question
```

### Get Interview Report

```http
GET /interviews/{interview_id}/report
```

---

## Future Improvements

* Voice-based interviews
* Real-time interviewer avatar
* WebSocket streaming
* Multi-language interviews
* Advanced scoring calibration
* Interview analytics dashboard
* Human-in-the-loop evaluation
* Support for multiple job families

---

## Results

The platform successfully supports:

* End-to-end interview generation
* Adaptive follow-up questioning
* Retrieval-grounded evaluation
* Automated recruiter reports
* Candidate feedback generation

The system demonstrates how modern LLM orchestration, retrieval systems, and agent workflows can be combined to create intelligent interview experiences.
