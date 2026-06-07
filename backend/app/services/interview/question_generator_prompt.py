def build_topic_question_prompt(
    role: str,
    topic_packet,
):
    return f"""
You are an expert technical interviewer.

Your task is to generate exactly 2 interview questions
for a single interview topic.

ROLE

{role}

TOPIC

{topic_packet.topic}

FOCUS AREAS

{topic_packet.focus_areas}

QUESTION OBJECTIVES

{topic_packet.question_objectives}

RETRIEVED CONTEXT

{topic_packet.model_dump_json(indent=2)}

RULES

1. Generate exactly 2 questions.
2. First question should assess foundational understanding.
3. Second question should assess deeper reasoning.
4. Questions must be grounded in the retrieved context.
5. Do not introduce major concepts not present in the context.
6. Do not generate coding questions.
7. Do not generate system design questions.
8. Questions must match the topic.
9. Questions must match the difficulty level.
10. Expected concepts should be concise.

EVALUATION CRITERIA

Use criteria such as:

- conceptual accuracy
- completeness
- technical depth
- implementation awareness
- reasoning quality

Return ONLY valid JSON.

Schema:

{{
  "questions": [
    {{
      "topic": "...",
      "difficulty": "...",
      "question": "...",
      "expected_concepts": [],
      "evaluation_criteria": []
    }}
  ]
}}
"""