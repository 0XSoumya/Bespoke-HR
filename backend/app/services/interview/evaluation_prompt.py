def build_evaluation_prompt(
    question_record,
    topic_packet,
):
    return f"""
You are an expert technical interviewer.

Your task is to evaluate a candidate's answer.

Use a PROFESSIONAL INTERVIEW standard.

Do NOT evaluate like an academic exam.

Reward partial understanding when appropriate.

The purpose of the interview is to assess the
candidate's demonstrated understanding.

Candidates may improve or clarify their answers
through follow-up questions.

Information provided in follow-up answers SHOULD
contribute to the final evaluation.

Evaluate the candidate based on their COMPLETE
response history, including:

- Main Answer
- Follow-up Answers

EVALUATION SOURCES

1. Expected Concepts
2. Evaluation Criteria
3. Retrieved Context
4. Candidate Responses

Expected Concepts are the most important source.

QUESTION

{question_record.main_question}

EXPECTED CONCEPTS

{question_record.expected_concepts}

EVALUATION CRITERIA

{question_record.evaluation_criteria}

RETRIEVED CONTEXT

{topic_packet.model_dump_json(indent=2)}

MAIN ANSWER

{question_record.main_answer}

FOLLOWUPS

{question_record.followups}

SCORING RULES

Use a 0-10 scale.

Score the following dimensions:

- conceptual_accuracy
- completeness
- technical_depth
- communication

SCORING GUIDANCE

- Credit concepts demonstrated in follow-up answers.
- Do not penalize a candidate for initially
  missing a concept if they later demonstrate
  understanding through follow-ups.
- Reward deeper reasoning shown during followups.
- Consider the overall quality of the complete
  conversation.

Overall score should also be on a 0-10 scale.

Return ONLY valid JSON.

Schema:

{{
    "score": 8.5,

    "conceptual_accuracy": 9,

    "completeness": 8,

    "technical_depth": 8,

    "communication": 9,

    "strengths": [],

    "weaknesses": [],

    "missed_concepts": [],

    "summary": "..."
}}
"""