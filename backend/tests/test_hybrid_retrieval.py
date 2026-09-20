from app.services.retrieval.retrieval_service import RetrievalService
from app.services.retrieval.query_expansion_service import QueryExpansionService
from app.services.interview.role_config import ROLE_CONFIGS


def test_retrieval_service_initialization():
    """Verify RetrievalService initializes and can perform basic search."""
    service = RetrievalService()
    assert service.index is not None
    assert len(service.chunks) > 0


def main():
    retrieval_service = RetrievalService()
    expansion_service = QueryExpansionService()

    role = "AI/ML Engineer"
    role_config = ROLE_CONFIGS.get(role, {})
    domain_filter = role_config.get("preferred_domains", [None])[0]

    query = "Retrieval Augmented Generation with FAISS"
    expanded_query = expansion_service.expand_query(query)
    print(f"Expanded Query: {expanded_query}")

    results = retrieval_service.hybrid_search(
        query=expanded_query,
        top_k=3,
        domain_filter=domain_filter,
    )
    print(f"Retrieved {len(results)} results.")


if __name__ == "__main__":
    main()