from datetime import datetime, timezone
from typing import Any, Optional

from app.core.database import db
from app.models.schemas.interview_state import InterviewState


class InterviewRepository:
    def __init__(self):
        self.collection = db.interviews

    async def create(self, state: InterviewState):
        now = datetime.now(timezone.utc)
        document = {
            "_id": state.session.interview_id,
            "candidate_id": state.candidate_id,
            "interviewer_id": getattr(state, "interviewer_id", None),
            "candidate_user_id": getattr(state, "candidate_user_id", None),
            "candidate_email": getattr(state, "candidate_email", None),
            "candidate_name": getattr(state, "candidate_name", None),
            "number_of_questions": getattr(state, "number_of_questions", 3),
            "scheduled_at": getattr(state, "scheduled_at", None),
            "role": state.role,
            "status": state.status,
            "state": state.model_dump(),
            "created_at": now,
            "updated_at": now,
        }
        await self.collection.insert_one(document)

    async def get(self, interview_id: str) -> Optional[InterviewState]:
        document = await self.collection.find_one({"_id": interview_id})
        if document is None:
            return None
        return InterviewState.model_validate(document["state"])

    async def get_raw_document(self, interview_id: str) -> Optional[dict[str, Any]]:
        return await self.collection.find_one({"_id": interview_id})

    async def update(self, state: InterviewState):
        now = datetime.now(timezone.utc)
        update_fields: dict[str, Any] = {
            "state": state.model_dump(),
            "status": state.status,
            "updated_at": now,
        }
        # If report exists in state, record summary fields for analytics
        if state.report and state.report.recruiter_report:
            update_fields["overall_score"] = state.report.recruiter_report.overall_score
            update_fields["recommendation"] = state.report.recruiter_report.recommendation

        await self.collection.update_one(
            {"_id": state.session.interview_id},
            {"$set": update_fields},
        )

    async def delete(self, interview_id: str):
        await self.collection.delete_one({"_id": interview_id})

    async def list_for_interviewer(
        self, interviewer_id: str, limit: int = 100
    ) -> list[dict[str, Any]]:
        cursor = self.collection.find(
            {"$or": [{"interviewer_id": interviewer_id}, {"interviewer_id": None}]},
            {"state": 0},
        ).sort("created_at", -1).limit(limit)
        return [doc async for doc in cursor]

    async def list_for_candidate(
        self,
        candidate_user_id: Optional[str] = None,
        candidate_email: Optional[str] = None,
        candidate_id: Optional[str] = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        conditions = []
        if candidate_user_id:
            conditions.append({"candidate_user_id": candidate_user_id})
        if candidate_email:
            conditions.append({"candidate_email": candidate_email.lower().strip()})
        if candidate_id:
            conditions.append({"candidate_id": candidate_id})

        if not conditions:
            return []

        cursor = self.collection.find(
            {"$or": conditions},
            {"state": 0},
        ).sort("created_at", -1).limit(limit)
        return [doc async for doc in cursor]

    async def list_all(self, limit: int = 100) -> list[dict[str, Any]]:
        cursor = self.collection.find({}, {"state": 0}).sort("created_at", -1).limit(limit)
        return [doc async for doc in cursor]

    async def get_analytics(self, interviewer_id: Optional[str] = None) -> dict[str, Any]:
        query = {}
        if interviewer_id:
            query = {"$or": [{"interviewer_id": interviewer_id}, {"interviewer_id": None}]}

        docs = [doc async for doc in self.collection.find(query)]

        total_interviews = len(docs)
        completed_interviews = sum(1 for d in docs if d.get("status") in ("completed", "report_generated"))
        in_progress_interviews = sum(1 for d in docs if d.get("status") in ("in_progress", "interview_created", "question_presented", "answer_processed", "followup_presented"))
        scheduled_interviews = sum(1 for d in docs if d.get("status") == "scheduled")

        scores = [
            d.get("overall_score")
            for d in docs
            if d.get("overall_score") is not None
        ]
        # Also check state if overall_score was not denormalized
        for d in docs:
            if d.get("overall_score") is None and "state" in d:
                report = d.get("state", {}).get("report")
                if report and "recruiter_report" in report:
                    score = report["recruiter_report"].get("overall_score")
                    if score is not None:
                        scores.append(score)

        avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0
        completion_rate = round((completed_interviews / total_interviews * 100), 1) if total_interviews else 0.0

        role_counts: dict[str, int] = {}
        for d in docs:
            role = d.get("role", "Unknown")
            role_counts[role] = role_counts.get(role, 0) + 1

        recommendation_counts: dict[str, int] = {}
        for d in docs:
            rec = d.get("recommendation")
            if not rec and "state" in d:
                rec = (
                    d.get("state", {})
                    .get("report", {})
                    .get("recruiter_report", {})
                    .get("recommendation")
                )
            if rec:
                recommendation_counts[rec] = recommendation_counts.get(rec, 0) + 1

        return {
            "total_interviews": total_interviews,
            "completed_interviews": completed_interviews,
            "in_progress_interviews": in_progress_interviews,
            "scheduled_interviews": scheduled_interviews,
            "average_score": avg_score,
            "completion_rate": completion_rate,
            "role_distribution": role_counts,
            "recommendation_distribution": recommendation_counts,
        }