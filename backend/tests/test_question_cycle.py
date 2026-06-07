from app.models.schemas.candidate_profile import (
    CandidateProfile,
    Project,
)

from app.services.interview.interview_engine import (
    InterviewEngine,
)

from app.services.interview.session_service import (
    SessionService,
)

from app.graph.interview_graph import (
    build_interview_graph,
)


def main():

    candidate_profile = (
        CandidateProfile(
            candidate_summary=(
                "AI student with experience "
                "in RAG systems and LLM applications."
            ),

            skills=[
                "Python",
                "RAG",
                "LangChain",
                "Embeddings",
            ],

            projects=[
                Project(
                    title="Medical RAG",
                    description=(
                        "Built a medical RAG system."
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

    print(
        "\nCreating interview..."
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

    session_service = (
        SessionService()
    )

    first_question = (
        session_service
        .get_current_question(
            state.session
        )
    )

    state.current_question = (
        first_question
    )

    print(
        "\nCurrent Question:"
    )

    print(
        first_question.main_question
    )

    mock_answer = """
RAG combines retrieval and generation.

A retriever first searches a
knowledge base for relevant
documents.

The retrieved documents are
added to the prompt and sent
to the LLM.

This improves factual grounding
and reduces hallucinations.

Common components include
embeddings, vector databases,
retrievers, and prompt assembly.
"""

    session_service.save_main_answer(
        state.session,
        mock_answer,
    )

    graph = (
        build_interview_graph()
    )

    print(
        "\nRunning question cycle..."
    )

    result = graph.invoke(
        state
    )

    print(
        "\nStatus:"
    )

    print(
        result["status"]
    )

    current_question = (
        result.get(
            "current_question"
        )
    )

    if current_question:

        print(
            "\nNext Question:"
        )

        print(
            current_question
            .main_question
        )

    else:

        print(
            "\nInterview Complete"
        )

    completed_count = sum(
        1
        for record in (
            result[
                "session"
            ]
            .question_records
        )
        if record.completed
    )

    print(
        "\nCompleted Questions:"
    )

    print(
        completed_count
    )

    first_record = (
        result[
            "session"
        ]
        .question_records[0]
    )

    print(
        "\nEvaluation:"
    )

    print(
        first_record.evaluation
    )


if __name__ == "__main__":
    main()