import math
import time
from typing import Any, Sequence

import numpy as np


def compute_recall_at_k(retrieved_indices: Sequence[int], relevant_indices: set[int], k: int) -> float:
    if not relevant_indices:
        return 0.0
    top_k = retrieved_indices[:k]
    hits = len(set(top_k) & relevant_indices)
    return hits / len(relevant_indices)


def compute_precision_at_k(retrieved_indices: Sequence[int], relevant_indices: set[int], k: int) -> float:
    if k <= 0:
        return 0.0
    top_k = retrieved_indices[:k]
    hits = len(set(top_k) & relevant_indices)
    return hits / k


def compute_hit_rate_at_k(retrieved_indices: Sequence[int], relevant_indices: set[int], k: int) -> float:
    top_k = retrieved_indices[:k]
    return 1.0 if (set(top_k) & relevant_indices) else 0.0


def compute_mrr(retrieved_indices: Sequence[int], relevant_indices: set[int], k: int) -> float:
    top_k = retrieved_indices[:k]
    for rank, idx in enumerate(top_k, start=1):
        if idx in relevant_indices:
            return 1.0 / rank
    return 0.0


def compute_ndcg_at_k(retrieved_indices: Sequence[int], relevant_indices: set[int], k: int) -> float:
    top_k = retrieved_indices[:k]
    dcg = 0.0
    for i, idx in enumerate(top_k, start=1):
        if idx in relevant_indices:
            dcg += 1.0 / math.log2(i + 1)

    idcg = sum(1.0 / math.log2(i + 1) for i in range(1, min(k, len(relevant_indices)) + 1))
    if idcg == 0.0:
        return 0.0
    return dcg / idcg


class RetrievalEvaluator:
    def __init__(self, retrieval_service=None):
        if retrieval_service is None:
            from app.services.retrieval.retrieval_service import RetrievalService
            retrieval_service = RetrievalService()
        self.retrieval_service = retrieval_service

    def evaluate_benchmark(
        self,
        benchmark_cases: list[dict[str, Any]],
        k_values: list[int] = [3, 5, 10],
        search_mode: str = "hybrid",
    ) -> dict[str, Any]:
        """
        Runs evaluation on benchmark cases and computes average metrics.
        Each test case must have:
          - 'query': str
          - 'relevant_indices': list[int] (indices of relevant chunks)
          - optional 'domain': str
        """
        max_k = max(k_values)
        latencies_ms: list[float] = []

        per_k_metrics: dict[int, dict[str, list[float]]] = {
            k: {
                "recall": [],
                "precision": [],
                "hit_rate": [],
                "mrr": [],
                "ndcg": [],
            }
            for k in k_values
        }

        query_results_detail: list[dict[str, Any]] = []

        for case in benchmark_cases:
            query = case["query"]
            relevant_set = set(case.get("relevant_indices", []))

            t0 = time.perf_counter()
            if search_mode == "hybrid":
                results = self.retrieval_service.hybrid_search(query, top_k=max_k)
            elif search_mode == "semantic":
                results = self.retrieval_service.semantic_search(query, top_k=max_k)
            else:
                results = self.retrieval_service.keyword_search(query, top_k=max_k)
            latency_ms = (time.perf_counter() - t0) * 1000.0
            latencies_ms.append(latency_ms)

            # Extract chunk index from results:
            # Result objects have 'metadata' or 'chunk', let's map to index in chunks
            retrieved_indices = []
            for r in results:
                # Find index in chunks
                chunk_str = r.get("chunk", "")
                try:
                    idx = self.retrieval_service.chunks.index(chunk_str)
                except ValueError:
                    idx = -1
                if idx >= 0:
                    retrieved_indices.append(idx)

            case_detail: dict[str, Any] = {
                "query": query,
                "domain": case.get("domain", "general"),
                "relevant_count": len(relevant_set),
                "latency_ms": round(latency_ms, 2),
                "metrics": {},
            }

            for k in k_values:
                rec = compute_recall_at_k(retrieved_indices, relevant_set, k)
                prec = compute_precision_at_k(retrieved_indices, relevant_set, k)
                hit = compute_hit_rate_at_k(retrieved_indices, relevant_set, k)
                mrr = compute_mrr(retrieved_indices, relevant_set, k)
                ndcg = compute_ndcg_at_k(retrieved_indices, relevant_set, k)

                per_k_metrics[k]["recall"].append(rec)
                per_k_metrics[k]["precision"].append(prec)
                per_k_metrics[k]["hit_rate"].append(hit)
                per_k_metrics[k]["mrr"].append(mrr)
                per_k_metrics[k]["ndcg"].append(ndcg)

                case_detail["metrics"][f"k={k}"] = {
                    "recall": round(rec, 4),
                    "precision": round(prec, 4),
                    "hit_rate": round(hit, 4),
                    "mrr": round(mrr, 4),
                    "ndcg": round(ndcg, 4),
                }

            query_results_detail.append(case_detail)

        summary_by_k = {}
        for k in k_values:
            summary_by_k[f"k={k}"] = {
                "recall": round(float(np.mean(per_k_metrics[k]["recall"])), 4),
                "precision": round(float(np.mean(per_k_metrics[k]["precision"])), 4),
                "hit_rate": round(float(np.mean(per_k_metrics[k]["hit_rate"])), 4),
                "mrr": round(float(np.mean(per_k_metrics[k]["mrr"])), 4),
                "ndcg": round(float(np.mean(per_k_metrics[k]["ndcg"])), 4),
            }

        return {
            "search_mode": search_mode,
            "num_test_queries": len(benchmark_cases),
            "k_values": k_values,
            "summary_metrics": summary_by_k,
            "latency": {
                "mean_ms": round(float(np.mean(latencies_ms)), 2),
                "median_ms": round(float(np.median(latencies_ms)), 2),
                "p95_ms": round(float(np.percentile(latencies_ms, 95)), 2),
                "min_ms": round(float(np.min(latencies_ms)), 2),
                "max_ms": round(float(np.max(latencies_ms)), 2),
            },
            "queries": query_results_detail,
        }
