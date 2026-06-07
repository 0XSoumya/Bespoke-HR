import json


def build_query_planner_prompt(
    role: str,
    interview_plan,
):
    topics = []

    for topic in interview_plan.topics:
        topics.append(
            {
                "topic": topic.topic,
                "priority": topic.priority,
                "difficulty": topic.difficulty,
            }
        )

    topics_json = json.dumps(
        topics,
        indent=2,
    )

    return f"""
You are an expert knowledge retrieval planner.

Your task is to generate retrieval plans that will be used
to search a vector database containing technical books,
documentation, educational material, and interview preparation resources.

The retrieved knowledge will later be used by a separate
interview question generation system.

You are NOT an interviewer.

You are NOT generating interview questions.

You are NOT evaluating candidates.

Your only responsibility is to generate high-quality
retrieval-oriented search queries.

For EACH topic generate:

1. Exactly 3 retrieval queries
2. 3-5 focus areas
3. 2-4 question objectives

RETRIEVAL QUERY RULES

The queries will be embedded and used to search a vector database.

Queries should:

- be search-oriented
- target technical concepts
- be optimized for semantic retrieval
- be specific enough to retrieve focused knowledge
- use noun phrases and concept phrases

Good retrieval queries:

- retrieval augmented generation architecture
- chunking strategies for rag
- embedding model selection
- hybrid retrieval techniques
- vector similarity search methods
- prompt design patterns
- llm evaluation metrics

Bad retrieval queries:

- What is RAG?
- How does chunking work?
- Explain embeddings.
- Why use vector databases?
- Describe prompt engineering.

Do NOT generate questions.

Do NOT start queries with:

- what
- why
- how
- when
- explain
- describe

FOCUS AREA RULES

Focus areas represent the major subtopics that should be explored
for the interview topic.

QUESTION OBJECTIVE RULES

Question objectives describe what the future interview questions
should assess.

Examples:

- assess conceptual understanding
- evaluate design reasoning
- evaluate implementation experience
- assess troubleshooting ability

Return ONLY valid JSON.

Schema:

{{
  "role": "{role}",
  "topic_plans": [
    {{
      "topic": "...",
      "priority": 10,
      "difficulty": "...",

      "queries": [
        "...",
        "...",
        "..."
      ],

      "focus_areas": [
        "...",
        "..."
      ],

      "question_objectives": [
        "...",
        "..."
      ]
    }}
  ]
}}

Topics:

{topics_json}
"""