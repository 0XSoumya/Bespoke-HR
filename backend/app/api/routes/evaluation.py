import json
from pathlib import Path
from typing import Any, Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.core.config.settings import BACKEND_DIR
from app.services.retrieval.evaluation import RetrievalEvaluator
from app.services.retrieval.retrieval_service import RetrievalService

router = APIRouter(prefix="/evaluation", tags=["evaluation"])

BENCHMARK_PATH = BACKEND_DIR / "knowledge_base" / "eval_benchmark.json"
RESULTS_PATH = BACKEND_DIR / "knowledge_base" / "eval_results.json"


@router.get("/retrieval")
async def get_retrieval_metrics(
    refresh: bool = Query(False, description="Whether to re-run the benchmark live"),
    mode: str = Query("hybrid", pattern="^(hybrid|semantic|keyword)$"),
) -> dict[str, Any]:
    """
    Returns retrieval evaluation metrics:
    - Recall@K, Precision@K, Hit Rate, MRR, NDCG@K for K in [3, 5, 10]
    - Latency distribution (mean, median, p95, min, max in ms)
    """
    if not refresh and RESULTS_PATH.exists() and mode == "hybrid":
        try:
            with open(RESULTS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    if not BENCHMARK_PATH.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation benchmark dataset not found",
        )

    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)

    try:
        rs = RetrievalService()
        evaluator = RetrievalEvaluator(rs)
        results = evaluator.evaluate_benchmark(cases, k_values=[3, 5, 10], search_mode=mode)
        if mode == "hybrid":
            with open(RESULTS_PATH, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Evaluation execution failed: {str(e)}",
        )
