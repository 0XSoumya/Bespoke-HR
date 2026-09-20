from typing import Optional
from app.models.schemas.interview_plan import (
    InterviewPlan,
    InterviewTopic,
)
from app.models.schemas.interview_profile import InterviewProfile
from app.services.interview.role_config import (
    ROLE_CONFIGS,
    NATURE_CONFIGS,
)


class InterviewPlannerService:
    def build_plan(
        self,
        target_role: str,
        candidate_profile,
        num_questions: int = 3,
        interview_profile: Optional[InterviewProfile] = None,
    ) -> InterviewPlan:
        matched_role = None
        for role_key in ROLE_CONFIGS:
            if role_key.lower() in target_role.lower() or target_role.lower() in role_key.lower():
                matched_role = role_key
                break

        if matched_role is None:
            matched_role = "AI/ML Engineer"

        role_config = ROLE_CONFIGS[matched_role]
        priority_topics = dict(role_config["priority_topics"])

        # If interview_profile specifies nature, blend nature-specific priorities
        nature = interview_profile.interview_nature if interview_profile else None
        if nature and nature in NATURE_CONFIGS:
            nature_topics = NATURE_CONFIGS[nature]["priority_topics"]
            for n_topic, n_pri in nature_topics.items():
                priority_topics[n_topic] = max(priority_topics.get(n_topic, 0), n_pri)

        competencies = {
            competency.lower()
            for competency in getattr(candidate_profile, "claimed_competencies", [])
        }

        strengths = {
            strength.lower()
            for strength in getattr(candidate_profile, "strengths", [])
        }

        profile_focus = [
            f.lower() for f in (interview_profile.focus_areas if interview_profile else [])
        ]

        topics = []
        difficulty = (
            interview_profile.difficulty
            if interview_profile and interview_profile.difficulty
            else getattr(candidate_profile, "experience_level", "intermediate")
        )

        for topic, base_priority in priority_topics.items():
            priority = base_priority
            topic_lower = topic.lower()

            for competency in competencies:
                if topic_lower in competency or competency in topic_lower:
                    priority += 2

            for strength in strengths:
                if topic_lower in strength or strength in topic_lower:
                    priority += 2

            for focus in profile_focus:
                if topic_lower in focus or focus in topic_lower:
                    priority += 3

            topics.append(
                InterviewTopic(
                    topic=topic,
                    priority=priority,
                    difficulty=difficulty,
                    source="role+profile+nature",
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