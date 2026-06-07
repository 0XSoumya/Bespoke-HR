from app.models.schemas.candidate_profile import (
    CandidateProfile,
    Project,
)

from app.services.interview.interview_planner_service import (
    InterviewPlannerService,
)

from app.services.interview.query_planner_service import (
    QueryPlannerService,
)

from app.services.interview.retrieval_orchestrator import (
    RetrievalOrchestrator,
)

from app.services.interview.question_generator_service import (
    QuestionGeneratorService,
)


def main():

    candidate_profile = (
        CandidateProfile(
            candidate_summary=(
                "AI/ML student with experience "
                "building RAG systems, LangChain "
                "applications, vector search "
                "pipelines, and LLM-powered tools."
            ),

            skills=[
                "Python",
                "LangChain",
                "LangGraph",
                "RAG",
                "Vector Databases",
                "Machine Learning",
                "FastAPI",
            ],

            projects=[
                Project(
                    title="Medical RAG System",
                    description=(
                        "Built a medical question-answering "
                        "system using retrieval augmented "
                        "generation and vector databases."
                    ),
                ),

                Project(
                    title="AI Interview System",
                    description=(
                        "Built an adaptive interview platform "
                        "with retrieval, question generation, "
                        "evaluation, and reporting."
                    ),
                ),

                Project(
                    title="Resume Analyzer",
                    description=(
                        "Extracted skills, projects, and "
                        "competencies from resumes using LLMs."
                    ),
                ),
            ],

            domains=[
                "Generative AI",
                "Machine Learning",
            ],

            claimed_competencies=[
                "RAG",
                "Embeddings",
                "LangChain",
                "LangGraph",
                "Prompt Engineering",
            ],

            experience_level=(
                "intermediate"
            ),

            education=[
                "B.Tech Computer Science"
            ],

            strengths=[
                "RAG",
                "Generative AI",
            ],
        )
    )

    role = "GenAI Engineer"

    print(
        "\n========================"
    )
    print(
        "INTERVIEW PLAN"
    )
    print(
        "========================\n"
    )

    planner = (
        InterviewPlannerService()
    )

    interview_plan = (
        planner.build_plan(
            role,
            candidate_profile,
        )
    )

    print(
        interview_plan.model_dump_json(
            indent=2
        )
    )

    print(
        "\n========================"
    )
    print(
        "QUERY PLAN"
    )
    print(
        "========================\n"
    )

    query_planner = (
        QueryPlannerService()
    )

    query_plan = (
        query_planner.build_query_plan(
            role,
            interview_plan,
        )
    )

    print(
        query_plan.model_dump_json(
            indent=2
        )
    )

    print(
        "\n========================"
    )
    print(
        "BUILDING RETRIEVAL CONTEXT..."
    )
    print(
        "========================\n"
    )

    retrieval = (
        RetrievalOrchestrator()
    )

    retrieval_context = (
        retrieval.build_context(
            query_plan
        )
    )

    print(
        "Retrieval context built."
    )

    print(
        "\n========================"
    )
    print(
        "QUESTION SET"
    )
    print(
        "========================\n"
    )

    generator = (
        QuestionGeneratorService()
    )

    question_set = (
        generator.generate_questions(
            retrieval_context
        )
    )

    print(
        question_set.model_dump_json(
            indent=2
        )
    )


if __name__ == "__main__":
    main()