def build_resume_parser_prompt(
    resume_text: str,
) -> str:

    return f"""
You are an expert technical recruiter.

Analyze the resume and extract information.

Return ONLY valid JSON.

Schema:

{{
    "candidate_summary": "...",

    "skills": [],

    "projects": [
        {{
            "title": "...",
            "description": "..."
        }}
    ],

    "domains": [],

    "claimed_competencies": [],

    "experience_level":
        "beginner | intermediate | advanced",

    "education": [],

    "strengths": []
}}

Rules:

1. Return valid JSON only.
2. No markdown.
3. No explanations.
4. Skills must be technical.
5. Claimed competencies should be interview-relevant.
6. Experience level must be:
   beginner, intermediate, or advanced.

Resume:

{resume_text}
"""