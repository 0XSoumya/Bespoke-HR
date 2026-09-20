from datetime import datetime, timezone
from typing import Any, Optional

from app.core.database import db
from app.models.schemas.interview_state import InterviewState


class InterviewRepository:
    @property
    def collection(self):
        return db.interviews

    async def create(self, state: InterviewState):
        now = datetime.now(timezone.utc)
        document = {
            "_id": state.session.interview_id,
            "candidate_id": state.candidate_id,
            "interviewer_id": getattr(state, "interviewer_id", None),
            "candidate_user_id": getattr(state, "candidate_user_id", None),
            "candidate_email": getattr(state, "candidate_email", None),
            "candidate_name": getattr(state, "candidate_name", None),
            "company": getattr(state, "company", "Target Company"),
            "interview_stage": (
                state.interview_profile.interview_stage
                if state.interview_profile
                else "Technical Round 1"
            ),
            "interview_nature": (
                state.interview_profile.interview_nature
                if state.interview_profile
                else "ML/AI Technical"
            ),
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
        if state.report:
            if state.report.preparation_report:
                update_fields["overall_score"] = state.report.preparation_report.overall_readiness_score
                update_fields["readiness_tier"] = state.report.preparation_report.readiness_tier
            elif state.report.recruiter_report:
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

        total = await self.collection.count_documents(query)
        completed = await self.collection.count_documents({**query, "status": "completed"})

        avg_pipeline = [
            {"$match": {**query, "overall_score": {"$exists": True, "$ne": None}}},
            {"$group": {"_id": None, "avg_score": {"$avg": "$overall_score"}}},
        ]
        avg_res = await self.collection.aggregate(avg_pipeline).to_list(1)
        avg_score = round(avg_res[0]["avg_score"], 2) if avg_res else 0.0

        return {
            "total_interviews": total,
            "completed_interviews": completed,
            "in_progress": total - completed,
            "average_score": avg_score,
        }