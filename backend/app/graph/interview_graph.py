from langgraph.graph import (
    StateGraph,
    END,
)

from app.models.schemas.interview_state import (
    InterviewState,
)

from app.services.interview.session_service import (
    SessionService,
)

from app.services.interview.evaluation_service import (
    EvaluationService,
)

from app.services.interview.report_service import (
    ReportService,
)

from app.services.interview.followup_service import (
    FollowupService,
)


session_service = (
    SessionService()
)

evaluation_service = (
    EvaluationService()
)

report_service = (
    ReportService()
)

followup_service = (
    FollowupService()
)


def process_answer_node(
    state: InterviewState,
):

    if state.pending_followup:

        state.status = (
            "followup_answer_received"
        )

    else:

        state.status = (
            "answer_processed"
        )

    return state

def answer_router(
    state: InterviewState,
):

    if state.pending_followup:

        return (
            "evaluate_question"
        )

    return (
        "followup_decision"
    )


def followup_decision_node(
    state: InterviewState,
):

    decision = (
        followup_service
        .generate_followup(
            state.current_question
        )
    )

    state.followup_decision = (
        decision
    )

    state.status = (
        "followup_decided"
    )

    return state


def present_followup_node(
    state: InterviewState,
):

    session_service.add_followup_question(
        state.session,
        state.followup_decision
        .followup_question,
    )

    state.pending_followup = (
        True
    )

    state.status = (
        "followup_presented"
    )

    return state


def evaluate_question_node(
    state: InterviewState,
):

    evaluation = (
        evaluation_service
        .evaluate_question(
            question_record=(
                state.current_question
            ),
            retrieval_context=(
                state.retrieval_context
            ),
        )
    )

    state.current_question.evaluation = (
        evaluation
    )

    state.pending_followup = (
        False
    )

    state.followup_decision = (
        None
    )

    state.status = (
        "question_evaluated"
    )

    return state


def advance_question_node(
    state: InterviewState,
):

    session_service.mark_question_complete(
        state.session
    )

    session_service.move_to_next_question(
        state.session
    )

    state.status = (
        "question_advanced"
    )

    return state


def present_next_question_node(
    state: InterviewState,
):

    current_question = (
        session_service
        .get_current_question(
            state.session
        )
    )

    state.current_question = (
        current_question
    )

    state.status = (
        "question_presented"
    )

    return state


def generate_report_node(
    state: InterviewState,
):

    report = (
        report_service
        .generate_report(
            state.session
            .question_records
        )
    )

    state.report = (
        report
    )

    state.status = (
        "report_generated"
    )

    return state


def followup_router(
    state: InterviewState,
):

    if (
        state.followup_decision
        and
        state.followup_decision
        .generate_followup
    ):
        return (
            "present_followup"
        )

    return (
        "evaluate_question"
    )


def completion_router(
    state: InterviewState,
):

    if (
        state.session.status
        == "completed"
    ):
        return (
            "generate_report"
        )

    return (
        "present_next_question"
    )


def build_interview_graph():

    graph = StateGraph(
        InterviewState
    )

    graph.add_node(
        "process_answer",
        process_answer_node,
    )

    graph.add_node(
        "followup_decision",
        followup_decision_node,
    )

    graph.add_node(
        "present_followup",
        present_followup_node,
    )

    graph.add_node(
        "evaluate_question",
        evaluate_question_node,
    )

    graph.add_node(
        "advance_question",
        advance_question_node,
    )

    graph.add_node(
        "present_next_question",
        present_next_question_node,
    )

    graph.add_node(
        "generate_report",
        generate_report_node,
    )

    graph.set_entry_point(
        "process_answer"
    )

    graph.add_conditional_edges(
        "process_answer",
        answer_router,
        {
            "followup_decision":
             "followup_decision",

            "evaluate_question":
             "evaluate_question",
        },
    )

    graph.add_conditional_edges(
        "followup_decision",
        followup_router,
        {
            "present_followup":
                "present_followup",

            "evaluate_question":
                "evaluate_question",
        },
    )

    graph.add_edge(
        "evaluate_question",
        "advance_question",
    )

    graph.add_conditional_edges(
        "advance_question",
        completion_router,
        {
            "present_next_question":
                "present_next_question",

            "generate_report":
                "generate_report",
        },
    )

    graph.add_edge(
        "present_followup",
        END,
    )

    graph.add_edge(
        "present_next_question",
        END,
    )

    graph.add_edge(
        "generate_report",
        END,
    )

    return graph.compile()