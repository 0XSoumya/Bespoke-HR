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

    engine = (
        InterviewEngine()
    )

    session_service = (
        SessionService()
    )

    graph = (
        build_interview_graph()
    )

    print(
        "\nCreating interview..."
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

    # --------------------------------------------------
    # First Answer
    # --------------------------------------------------

    weak_answer = (
        "RAG retrieves documents "
        "and uses them."
    )

    session_service.save_main_answer(
        state.session,
        weak_answer,
    )

    print(
        "\nSubmitting weak answer..."
    )

    result = graph.invoke(
        state
    )

    print(
        "\nStatus After First Run:"
    )

    print(
        result["status"]
    )

    current_question = (
        result["current_question"]
    )

    if (
        current_question.followups
    ):
        print(
            "\nFollowup #1:"
        )

        print(
            current_question
            .followups[-1]
            .question
        )

    # --------------------------------------------------
    # Followup Answer #1
    # --------------------------------------------------

    followup_answer_1 = """
RAG retrieves relevant documents
from a knowledge base and injects
them into the prompt before the
LLM generates a response.
"""

    print(
        "\nSubmitting followup answer #1..."
    )

    session_service.save_followup_answer(
        result["session"],
        followup_answer_1,
    )

    result["pending_followup"] = False

    result = graph.invoke(
        result
    )

    print(
        "\nStatus After Second Run:"
    )

    print(
        result["status"]
    )

    current_question = (
        result["current_question"]
    )

    if (
        result["status"]
        == "followup_presented"
    ):
        print(
            "\nFollowup #2:"
        )

        print(
            current_question
            .followups[-1]
            .question
        )

    first_record = (
        result["session"]
        .question_records[0]
    )

    print(
        "\nCurrent Followups:"
    )

    print(
        len(
            first_record.followups
        )
    )

    # --------------------------------------------------
    # Followup Answer #2
    # --------------------------------------------------

    if (
        result["status"]
        == "followup_presented"
    ):

        followup_answer_2 = """
Unlike traditional language models,
RAG accesses external knowledge at
inference time using embeddings and
retrieval systems.

This improves factual accuracy,
reduces hallucinations, and allows
knowledge updates without retraining
the model.
"""

        print(
            "\nSubmitting followup answer #2..."
        )

        session_service.save_followup_answer(
            result["session"],
            followup_answer_2,
        )

        result["pending_followup"] = False

        result = graph.invoke(
            result
        )

        print(
            "\nStatus After Third Run:"
        )

        print(
            result["status"]
        )

    # --------------------------------------------------
    # Final Validation
    # --------------------------------------------------

    first_record = (
        result["session"]
        .question_records[0]
    )

    print(
        "\nFinal Followup Count:"
    )

    print(
        len(
            first_record.followups
        )
    )

    print(
        "\nEvaluation:"
    )

    print(
        first_record.evaluation
    )

    assert (
        first_record.evaluation
        is not None
    )

    assert (
        first_record.completed
        is True
    )

    print(
        "\nCompleted:"
    )

    print(
        first_record.completed
    )

    if (
        result["session"].status
        != "completed"
    ):
        print(
            "\nNext Question:"
        )

        print(
            result[
                "current_question"
            ].main_question
        )

    print(
        "\nTEST PASSED"
    )


if __name__ == "__main__":
    main()