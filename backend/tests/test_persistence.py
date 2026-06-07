import asyncio

from app.models.schemas.candidate_profile import (
    CandidateProfile,
)

from app.services.interview.interview_engine import (
    InterviewEngine,
)

from app.services.interview.interview_persistence_service import (
    InterviewPersistenceService,
)


async def main():

    candidate_profile = (
        CandidateProfile(
            candidate_summary=(
                "Persistence test"
            ),
            skills=[
                "Python"
            ],
            projects=[],
            domains=[
                "AI"
            ],
            claimed_competencies=[
                "RAG"
            ],
            experience_level=(
                "intermediate"
            ),
            education=[
                "B.Tech"
            ],
            strengths=[
                "Python"
            ],
        )
    )

    engine = (
        InterviewEngine()
    )

    persistence = (
        InterviewPersistenceService()
    )

    print(
        "\nCreating interview..."
    )

    state = (
        engine.create_interview(
            candidate_id=(
                "test_candidate"
            ),
            role=(
                "GenAI Engineer"
            ),
            candidate_profile=(
                candidate_profile
            ),
        )
    )

    interview_id = (
        state.session
        .interview_id
    )

    print(
        "\nSaving interview..."
    )

    await (
        persistence
        .save_interview(
            state
        )
    )

    print(
        "\nLoading interview..."
    )

    loaded_state = await (
        persistence
        .load_interview(
            interview_id
        )
    )

    assert (
        loaded_state
        is not None
    )

    assert (
        loaded_state.role
        == state.role
    )

    assert (
        loaded_state
        .candidate_id
        == state.candidate_id
    )

    assert (
        loaded_state
        .session
        .interview_id
        == interview_id
    )

    print(
        "\nInterview ID:"
    )

    print(
        interview_id
    )

    print(
        "\nTEST PASSED"
    )


if __name__ == "__main__":
    asyncio.run(
        main()
    )