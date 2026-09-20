def build_report_prompt(
    evaluations_json: str,
    company: str = "Target Company",
    role: str = "Candidate",
    stage: str = "Technical Round 1",
    nature: str = "ML/AI Technical",
    company_insights_text: str = "",
) -> str:
    return f"""You are a master technical interview coach and career preparation expert.
Generate a comprehensive, evidence-grounded candidate preparation report for:
Company: {company}
Target Role: {role}
Interview Stage: {stage}
Round Nature: {nature}
Company Context: {company_insights_text}

Analyze the candidate's performance across the questions and follow-ups.

Produce a JSON response with BOTH `preparation_report` (primary candidate prep guide) and `candidate_report`:
{{
  "preparation_report": {{
    "overall_readiness_score": 8.2,
    "readiness_tier": "Strong Baseline",
    "executive_summary": "Encouraging, actionable 2-3 sentence overview of candidate readiness for {company} {stage}.",
    "strengths": [
      "Concrete demonstrated strength 1",
      "Concrete demonstrated strength 2"
    ],
    "priority_gaps": [
      "Key gap or missing concept 1 to review before the interview",
      "Key gap 2"
    ],
    "topic_breakdown": {{
      "Topic A": 8.5
    }},
    "nature_rubric_scores": {{
      "Problem Solving": 8.0,
      "Technical Depth": 8.5,
      "Communication": 9.0
    }},
    "company_context_insights": [
      "Insight on how this performance aligns with {company}'s specific interview culture and expectations"
    ],
    "recommended_actions": [
      "Specific, actionable prep task 1 to prepare for {company}",
      "Specific practice recommendation 2"
    ],
    "question_reviews": []
  }},
  "candidate_report": {{
    "overall_score": 8.2,
    "strengths": ["..."],
    "areas_for_improvement": ["..."],
    "learning_recommendations": ["..."],
    "summary": "..."
  }},
  "recruiter_report": {{
    "overall_score": 8.2,
    "topic_scores": {{}},
    "strengths": [],
    "weaknesses": [],
    "recommendation": "Ready for Interview",
    "summary": "..."
  }}
}}

Return ONLY valid JSON.

Evaluations and Answer Details:
{evaluations_json}
"""