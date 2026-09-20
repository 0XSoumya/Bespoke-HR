import json
from collections import defaultdict
from typing import Optional

from app.models.schemas.interview_report import (
    InterviewReport,
    PreparationReport,
    CandidateReport,
    RecruiterReport,
    QuestionPreparationReview,
)
from app.models.schemas.interview_profile import InterviewProfile
from app.services.llm.groq_service import GroqService
from app.services.interview.report_prompt import build_report_prompt


class ReportService:
    def __init__(self):
        self.llm = GroqService()

    def generate_report(
        self,
        question_records,
        interview_profile: Optional[InterviewProfile] = None,
    ) -> InterviewReport:
        evaluations = []
        topic_scores = defaultdict(list)
        question_reviews: list[QuestionPreparationReview] = []

        for record in question_records:
            eval_data = record.evaluation.model_dump() if record.evaluation else {}
            evaluations.append({
                "question_id": record.question_id,
                "topic": record.topic,
                "difficulty": record.difficulty,
                "main_question": record.main_question,
                "main_answer": record.main_answer,
                "followups": [
                    {"question": f.question, "answer": f.answer}
                    for f in getattr(record, "followups", [])
                ],
                "evaluation": eval_data,
            })

            score = record.evaluation.score if record.evaluation else 7.0
            topic_scores[record.topic].append(score)

            question_reviews.append(
                QuestionPreparationReview(
                    question_id=record.question_id,
                    topic=record.topic,
                    main_question=record.main_question,
                    candidate_answer=record.main_answer,
                    followups=[
                        {"question": f.question, "answer": f.answer}
                        for f in getattr(record, "followups", [])
                    ],
                    score=score,
                    strengths=record.evaluation.strengths if record.evaluation else [],
                    gaps=record.evaluation.weaknesses if record.evaluation else [],
                    model_advice=record.evaluation.summary if record.evaluation else "",
                    evidence=record.evaluation.evidence if record.evaluation else [],
                )
            )

        avg_topic_scores = {}
        for topic, scores in topic_scores.items():
            avg_topic_scores[topic] = round(sum(scores) / len(scores), 2)

        overall_score = (
            round(sum(avg_topic_scores.values()) / len(avg_topic_scores), 2)
            if avg_topic_scores
            else 7.5
        )

        company = interview_profile.company if interview_profile else "Target Company"
        role = interview_profile.target_role if interview_profile else "Engineer"
        stage = interview_profile.interview_stage if interview_profile else "Technical Round 1"
        nature = interview_profile.interview_nature if interview_profile else "ML/AI Technical"
        company_insights = (
            " ".join(interview_profile.company_insights)
            if interview_profile and interview_profile.company_insights
            else ""
        )

        payload = {
            "overall_calculated_score": overall_score,
            "topic_scores": avg_topic_scores,
            "evaluations": evaluations,
        }

        try:
            prompt = build_report_prompt(
                evaluations_json=json.dumps(payload, indent=2),
                company=company,
                role=role,
                stage=stage,
                nature=nature,
                company_insights_text=company_insights,
            )
            response = self.llm.invoke(prompt)

            cleaned = response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            parsed_json = json.loads(cleaned.strip())

            report = InterviewReport.model_validate(parsed_json)
            if report.preparation_report:
                report.preparation_report.question_reviews = question_reviews
                if interview_profile and interview_profile.supporting_evidence:
                    report.preparation_report.evidence_citations = interview_profile.supporting_evidence
                if not report.preparation_report.topic_breakdown:
                    report.preparation_report.topic_breakdown = avg_topic_scores
            return report

        except Exception as e:
            # Fallback deterministic report generation if LLM fails
            tier = (
                "Interview Ready"
                if overall_score >= 8.5
                else "Strong Baseline"
                if overall_score >= 7.0
                else "Needs Targeted Practice"
            )

            prep_rep = PreparationReport(
                overall_readiness_score=overall_score,
                readiness_tier=tier,
                executive_summary=(
                    f"Candidate demonstrated a {tier.lower()} for {company} {stage} ({nature}). "
                    f"Core foundational competencies scored {overall_score}/10."
                ),
                strengths=[
                    f"Demonstrated solid grasp of {topic}" for topic in avg_topic_scores.keys()
                ],
                priority_gaps=[
                    "Deepen edge-case coverage and architectural trade-off justification"
                ],
                topic_breakdown=avg_topic_scores,
                nature_rubric_scores={"Technical Depth": overall_score, "Communication": 8.0},
                company_context_insights=[
                    f"Aligned with {company} expectations for {nature} interviews."
                ],
                recommended_actions=[
                    f"Review target questions for {company} {stage}.",
                    "Practice structured reasoning before writing code/answers.",
                ],
                question_reviews=question_reviews,
                evidence_citations=(
                    interview_profile.supporting_evidence if interview_profile else []
                ),
            )

            cand_rep = CandidateReport(
                overall_score=overall_score,
                strengths=prep_rep.strengths,
                areas_for_improvement=prep_rep.priority_gaps,
                learning_recommendations=prep_rep.recommended_actions,
                summary=prep_rep.executive_summary,
            )

            rec_rep = RecruiterReport(
                overall_score=overall_score,
                topic_scores=avg_topic_scores,
                strengths=prep_rep.strengths,
                weaknesses=prep_rep.priority_gaps,
                recommendation="Ready for Interview",
                summary=prep_rep.executive_summary,
            )

            return InterviewReport(
                preparation_report=prep_rep,
                candidate_report=cand_rep,
                recruiter_report=rec_rep,
            )