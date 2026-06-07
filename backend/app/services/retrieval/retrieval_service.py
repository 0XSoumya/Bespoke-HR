import json

import faiss
import numpy as np
from rank_bm25 import BM25Okapi

from app.services.retrieval.voyage_embedding_service import (
    VoyageEmbeddingService,
)

class RetrievalService:
    def __init__(
        self,
        faiss_path="knowledge_base/faiss.index",
        chunks_path="knowledge_base/chunks.json",
        metadata_path="knowledge_base/metadata.json",
    ):
        self.index = faiss.read_index(faiss_path)

        with open(chunks_path, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        self.embedding_service = VoyageEmbeddingService()

        tokenized_chunks = [
            chunk.lower().split()
            for chunk in self.chunks
        ]

        self.bm25 = BM25Okapi(
            tokenized_chunks
        )

    def semantic_search(
        self,
        query,
        top_k=10,
    ):
        query_embedding = (
            self.embedding_service
            .embed_query(query)
        )

        distances, indices = (
            self.index.search(
                np.array(
                    [query_embedding]
                ).astype(
                    "float32"
                ),
                top_k,
            )
        )

        results = []

        for idx, score in zip(
            indices[0],
            distances[0],
        ):

            if idx < 0:
                continue

            results.append(
                {
                    "chunk": (
                        self.chunks[idx]
                    ),
                    "metadata": (
                        self.metadata[idx]
                    ),
                    "score": float(
                        score
                    ),
                    "retrieval_type":
                        "semantic",
                }
            )

        return results

    def keyword_search(
        self,
        query,
        top_k=10,
    ):
        tokenized_query = (
            query.lower().split()
        )

        scores = (
            self.bm25.get_scores(
                tokenized_query
            )
        )

        ranked_indices = (
            np.argsort(scores)[::-1][
                :top_k
            ]
        )

        results = []

        for idx in ranked_indices:
            results.append(
                {
                    "chunk": (
                        self.chunks[idx]
                    ),
                    "metadata": (
                        self.metadata[idx]
                    ),
                    "score": float(
                        scores[idx]
                    ),
                    "retrieval_type":
                        "keyword",
                }
            )

        return results

    def hybrid_search(
        self,
        query,
        top_k=10,
        domain_filter=None,
        difficulty_filter=None,
    ):
        semantic_results = (
            self.semantic_search(
                query,
                top_k=top_k,
            )
        )

        keyword_results = (
            self.keyword_search(
                query,
                top_k=top_k,
            )
        )

        rrf_scores = {}

        k = 60

        for rank, result in enumerate(
            semantic_results,
            start=1,
        ):
            chunk = result["chunk"]

            rrf_scores.setdefault(
                chunk,
                {
                    "score": 0,
                    "result": result,
                },
            )

            rrf_scores[chunk][
                "score"
            ] += (
                1 / (k + rank)
            )

        for rank, result in enumerate(
            keyword_results,
            start=1,
        ):
            chunk = result["chunk"]

            if (
                chunk
                not in rrf_scores
            ):
                rrf_scores[
                    chunk
                ] = {
                    "score": 0,
                    "result": result,
                }

            rrf_scores[chunk][
                "score"
            ] += (
                1 / (k + rank)
            )

        ranked_results = sorted(
            rrf_scores.values(),
            key=lambda item: (
                item["score"]
            ),
            reverse=True,
        )

        filtered = []

        for item in ranked_results:

            result = item["result"]

            metadata = result[
                "metadata"
            ]

            if domain_filter:
                if (
                    domain_filter
                    not in metadata[
                        "domains"
                    ]
                ):
                    continue

            if difficulty_filter:
                if (
                    metadata[
                        "difficulty"
                    ]
                    != difficulty_filter
                ):
                    continue

            result[
                "rrf_score"
            ] = item["score"]

            filtered.append(
                result
            )

        return filtered[:top_k] 