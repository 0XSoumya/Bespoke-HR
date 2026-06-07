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
        "\nQuestion:"
    )

    print(
        first_question.main_question
    )

    weak_answer = (
        "RAG retrieves documents "
        "and uses them."
    )

    session_service.save_main_answer(
        state.session,
        weak_answer,
    )

    graph = (
        build_interview_graph()
    )

    print(
        "\nRunning graph..."
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

    print(
        "\nPending Followup:"
    )

    print(
        result["pending_followup"]
    )

    decision = (
        result[
            "followup_decision"
        ]
    )

    print(
        "\nFollowup Decision:"
    )

    print(
        decision
    )

    current_question = (
        result[
            "current_question"
        ]
    )

    print(
        "\nFollowup Count:"
    )

    print(
        len(
            current_question
            .followups
        )
    )

    if (
        current_question
        .followups
    ):
        print(
            "\nGenerated Followup:"
        )

        print(
            current_question
            .followups[-1]
            .question
        )

    assert (
        result["status"]
        == "followup_presented"
    )

    assert (
        result["pending_followup"]
        is True
    )

    assert (
        decision
        is not None
    )

    assert (
        decision.generate_followup
        is True
    )

    assert (
        len(
            current_question
            .followups
        )
        == 1
    )

    print(
        "\nTEST PASSED"
    )


if __name__ == "__main__":
    main()