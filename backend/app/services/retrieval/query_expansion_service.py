class QueryExpansionService:
    def __init__(self):
        self.concept_map = {
            "faiss": [
                "vector retrieval",
                "ann indexing",
                "similarity search",
                "vector database",
            ],
            "rag": [
                "retrieval augmented generation",
                "context retrieval",
                "vector search",
            ],
            "fastapi": [
                "api development",
                "backend framework",
                "python api",
            ],
            "docker": [
                "containerization",
                "deployment",
                "containers",
            ],
        }

    def expand_query(self, query: str):
        expanded_terms = [query]

        query_lower = query.lower()

        for concept, related_terms in self.concept_map.items():
            if concept in query_lower:
                expanded_terms.extend(related_terms)

        return " ".join(expanded_terms)