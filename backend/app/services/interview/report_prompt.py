def build_report_prompt(
    evaluations,
):
    return f"""
You are an expert technical interviewer.

Your task is to generate:

1. Recruiter Report
2. Candidate Report

Use the supplied question evaluations.

RECRUITER REPORT

Include:

- overall score
- topic scores
- strengths
- weaknesses
- recommendation

Recommendations must be one of:

- Strong Hire
- Hire
- Borderline
- No Hire

CANDIDATE REPORT

Include:

- overall score
- strengths
- areas for improvement
- learning recommendations

Return ONLY valid JSON.

Schema:

{{
  "recruiter_report": {{
    "overall_score": 8.5,
    "topic_scores": {{}},
    "strengths": [],
    "weaknesses": [],
    "recommendation": "Hire",
    "summary": "..."
  }},

  "candidate_report": {{
    "overall_score": 8.5,
    "strengths": [],
    "areas_for_improvement": [],
    "learning_recommendations": [],
    "summary": "..."
  }}
}}

Evaluations:

{evaluations}
"""