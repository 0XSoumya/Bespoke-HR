from app.services.resume.resume_parser_service import (
    ResumeParserService,
)

resume_text = """
Soumya Sahoo

B.Tech Computer Science (AI & ML Specialization)

SKILLS

Python
Machine Learning
Deep Learning
LangChain
LangGraph
FAISS
ChromaDB
FastAPI
MongoDB
Docker
Git
Streamlit
RAG
Prompt Engineering

PROJECTS

Medical Research Assistant

Built a RAG-based medical research assistant using
LangGraph, LangChain, FAISS, and Gemini.
The system retrieved and analyzed medical papers
from the internet and generated grounded responses.

AI Interview System

Designed and implemented an AI-powered adaptive
interview platform capable of resume analysis,
retrieval-grounded question generation,
candidate evaluation, and report generation.

Personal Finance Assistant

Built a personal finance application using LangChain
that analyzes spending behavior and provides
financial insights for Indian users.

Visual Book Recommender

Built a visual recommendation system using
ResNet and FAISS with over 1200 book covers
across multiple genres.

EXPERIENCE

Built multiple AI and RAG applications involving
retrieval systems, embeddings, vector databases,
LLM orchestration, and backend APIs.

EDUCATION

Bachelor of Technology in Computer Science
(AI & ML Specialization)
"""

service = ResumeParserService()

profile = service.parse_resume(
    resume_text=resume_text
)

print("\nCandidate Profile\n")
print("=" * 80)

print(
    profile.model_dump_json(
        indent=2
    )
)