from typing import Optional
from app.models.schemas.interview_profile import InterviewProfile


def build_evaluation_prompt(
    question_record,
    topic_packet,
    interview_profile: Optional[InterviewProfile] = None,
) -> str:
    company = interview_profile.company if interview_profile else "Target Company"
    stage = interview_profile.interview_stage if interview_profile else "Technical Round 1"
    nature = interview_profile.interview_nature if interview_profile else "ML/AI Technical"
    rubric_items = (
        "\n- " + "\n- ".join(interview_profile.rubric_criteria)
        if interview_profile and interview_profile.rubric_criteria
        else "- Technical correctness\n- Problem-solving structure\n- Communication clarity"
    )

    context_json = (
        topic_packet.model_dump_json(indent=2)
        if hasattr(topic_packet, "model_dump_json")
        else str(topic_packet)
    )

    followups_text = "\n".join(
        [f"Follow-up: {f.question}\nAnswer: {f.answer}" for f in getattr(question_record, "followups", [])]
    ) or "None"

    return f"""You are an expert technical interviewer and interview coach evaluating a candidate for:
Company: {company}
Interview Stage: {stage}
Round Nature: {nature}

STAGE & NATURE RUBRIC CRITERIA:
{rubric_items}

EVALUATION PRINCIPLES:
- Professional interview standard (not an academic exam).
- Evaluate based on the COMPLETE response history (Main answer + Follow-up answers).
- Credit candidate clarifications and deeper reasoning demonstrated during follow-ups.
- Identify specific factual quotes or arguments as evidence.

QUESTION:
{question_record.main_question}

EXPECTED CONCEPTS:
{question_record.expected_concepts}

EVALUATION CRITERIA:
{question_record.evaluation_criteria}

RETRIEVED TECHNICAL KNOWLEDGE:
{context_json}

MAIN CANDIDATE ANSWER:
{question_record.main_answer}

FOLLOW-UP CONVERSATION:
{followups_text}

SCORING (0.0 to 10.0 scale):
Return ONLY valid JSON matching this schema:
{{
    "score": 8.5,
    "conceptual_accuracy": 9.0,
    "completeness": 8.0,
    "technical_depth": 8.5,
    "communication": 9.0,
    "rubric_scores": {{
        "Correctness": 9.0,
        "Depth": 8.5,
        "Trade-off Analysis": 8.0
    }},
    "strengths": [
        "Identified clear trade-off between latency and accuracy"
    ],
    "weaknesses": [
        "Did not discuss memory bottlenecks under high concurrency"
    ],
    "missed_concepts": [],
    "evidence": [
        "Direct quote or factual reference from candidate answer demonstrating competency"
    ],
    "summary": "2-3 sentences summarizing performance on this question."
}}
"""