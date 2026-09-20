from app.models.schemas.interview_plan import (
    InterviewPlan,
    InterviewTopic,
)

from app.services.interview.role_config import (
    ROLE_CONFIGS,
)


class InterviewPlannerService:
    def build_plan(
        self,
        target_role: str,
        candidate_profile,
        num_questions: int = 3,
    ) -> InterviewPlan:

        matched_role = None
        for role_key in ROLE_CONFIGS:
            if role_key.lower() == target_role.lower():
                matched_role = role_key
                break

        if matched_role is None:
            matched_role = "AI/ML Engineer"

        role_config = ROLE_CONFIGS[matched_role]

        priority_topics = (
            role_config["priority_topics"]
        )

        competencies = {
            competency.lower()
            for competency in
            candidate_profile.claimed_competencies
        }

        strengths = {
            strength.lower()
            for strength in
            candidate_profile.strengths
        }

        topics = []

        for (
            topic,
            base_priority,
        ) in priority_topics.items():

            priority = base_priority

            topic_lower = topic.lower()

            for competency in competencies:
                if topic_lower in competency:
                    priority += 2

            for strength in strengths:
                if topic_lower in strength:
                    priority += 2

            topics.append(
                InterviewTopic(
                    topic=topic,
                    priority=priority,
                    difficulty=(
                        candidate_profile
                        .experience_level
                    ),
                    source="role+resume",
                )
            )

        topics.sort(
            key=lambda x: x.priority,
            reverse=True,
        )

        if num_questions and num_questions > 0:
            topics = topics[:num_questions]

        return InterviewPlan(
            role=matched_role,
            topics=topics,
        )