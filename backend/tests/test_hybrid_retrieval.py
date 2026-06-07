from app.services.retrieval.query_expansion_service import (
    QueryExpansionService,
)
from app.services.retrieval.retrieval_service import RetrievalService
from app.services.retrieval.concept_normalizer import (
    ConceptNormalizer,
)
from app.services.retrieval.topic_sampler import TopicSampler
from app.services.retrieval.role_config import ROLE_CONFIGS


def main():
    retrieval_service = RetrievalService()

    expansion_service = QueryExpansionService()

    normalizer = ConceptNormalizer()

    sampler = TopicSampler()

    role = input(
        "Enter role (AI/ML Engineer or Backend Engineer): "
    )

    role_config = ROLE_CONFIGS.get(role)

    if not role_config:
        print("Invalid role")
        return

    while True:
        query = input("\nQuery: ")

        if query.lower() == "exit":
            break

        expanded_query = expansion_service.expand_query(query)

        concepts = expanded_query.split()

        normalized = normalizer.normalize(concepts)

        sampled_topics = sampler.sample_topics(
            available_topics=normalized,
            role=role,
            k=5,
        )

        final_query = " ".join(sampled_topics)

        print(f"\nExpanded Query:\n{expanded_query}\n")

        print(f"\nNormalized Concepts:\n{normalized}\n")

        print(f"\nSampled Topics:\n{sampled_topics}\n")

        results = retrieval_service.hybrid_search(
            query=final_query,
            top_k=5,
            domain_filter=role_config["preferred_domains"][0],
            difficulty_filter=role_config["difficulty"],
        )

        print("\nResults:\n")

        for i, result in enumerate(results):
            print("=" * 80)
            print(f"Result {i + 1}")
            print(f"Type: {result['retrieval_type']}")
            print(f"Metadata: {result['metadata']}")
            print("-" * 80)
            print(result["chunk"][:1000])
            print("\n")


if __name__ == "__main__":
    main()