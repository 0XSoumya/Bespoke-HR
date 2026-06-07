from collections import defaultdict

from app.models.schemas.context_packet import (
    RetrievalContext,
    RetrievedChunk,
    TopicContextPacket,
)

from app.services.retrieval.retrieval_service import (
    RetrievalService,
)


class RetrievalOrchestrator:
    def __init__(self):
        self.retrieval_service = (
            RetrievalService()
        )

    def build_context(
        self,
        query_plan,
    ) -> RetrievalContext:

        topic_packets = []

        for topic_plan in (
            query_plan.topic_plans
        ):

            chunk_registry = {}

            retrieval_counts = defaultdict(
                int
            )

            for query in (
                topic_plan.queries
            ):

                results = (
                    self.retrieval_service
                    .hybrid_search(
                        query=query,
                        top_k=5,
                    )
                )

                for result in results:

                    chunk = result["chunk"]

                    retrieval_counts[
                        chunk
                    ] += 1

                    if (
                        chunk
                        not in chunk_registry
                    ):
                        chunk_registry[
                            chunk
                        ] = result

            ranked_chunks = sorted(
                chunk_registry.values(),
                key=lambda item: (
                    retrieval_counts[
                        item["chunk"]
                    ]
                ),
                reverse=True,
            )

            ranked_chunks = (
                ranked_chunks[:10]
            )

            retrieved_chunks = []

            for result in ranked_chunks:

                retrieved_chunks.append(
                    RetrievedChunk(
                        chunk=result["chunk"],
                        metadata=result[
                            "metadata"
                        ],
                        retrieval_count=(
                            retrieval_counts[
                                result["chunk"]
                            ]
                        ),
                    )
                )

            topic_packets.append(
                TopicContextPacket(
                    topic=topic_plan.topic,
                    focus_areas=(
                        topic_plan
                        .focus_areas
                    ),
                    question_objectives=(
                        topic_plan
                        .question_objectives
                    ),
                    retrieved_chunks=(
                        retrieved_chunks
                    ),
                )
            )

        return RetrievalContext(
            role=query_plan.role,
            topic_packets=topic_packets,
        )