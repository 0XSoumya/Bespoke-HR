from app.models.schemas.candidate_profile import (
    CandidateProfile,
    Project,
)

from app.services.interview.interview_engine import (
    InterviewEngine,
)

from app.graph.interview_graph import (
    build_interview_graph,
)


def main():

    candidate_profile = (
        CandidateProfile(
            candidate_summary=(
                "AI student"
            ),
            skills=[
                "Python",
                "RAG",
                "LangChain",
            ],
            projects=[
                Project(
                    title="Medical RAG",
                    description=(
                        "Built a medical RAG system"
                    ),
                ),
            ],
            domains=[
                "Generative AI",
            ],
            claimed_competencies=[
                "RAG",
                "Embeddings",
            ],
            experience_level=(
                "intermediate"
            ),
            education=[
                "B.Tech"
            ],
            strengths=[
                "RAG"
            ],
        )
    )

    engine = (
        InterviewEngine()
    )

    state = (
        engine.create_interview(
            candidate_id="test",
            role="GenAI Engineer",
            candidate_profile=(
                candidate_profile
            ),
        )
    )

    graph = (
        build_interview_graph()
    )

    result = graph.invoke(
        state
    )

    print(
        result["status"]
    )

    print(
        result["current_question"]
    )


if __name__ == "__main__":
    main()