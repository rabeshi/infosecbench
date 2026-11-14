from __future__ import annotations

from collections import defaultdict
from statistics import mean, median
from typing import Any


def summarize_scores(evaluations: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate a list of evaluation dicts (as produced by ScenarioEvaluation.to_dict())."""
    normalized = [float(e.get("normalized_score", 0.0)) for e in evaluations]
    passed = [bool(e.get("passed", False)) for e in evaluations]
    return {
        "count": len(evaluations),
        "mean_normalized_score": round(mean(normalized), 4) if normalized else 0.0,
        "median_normalized_score": round(median(normalized), 4) if normalized else 0.0,
        "min_normalized_score": min(normalized) if normalized else 0.0,
        "max_normalized_score": max(normalized) if normalized else 0.0,
        "pass_rate": round(sum(passed) / len(passed), 4) if passed else 0.0,
    }


def group_summary(evaluations: list[dict[str, Any]], group_by: str) -> dict[str, dict[str, Any]]:
    """Summarize scores grouped by a top-level evaluation field (e.g. 'category', 'difficulty')."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for evaluation in evaluations:
        groups[str(evaluation.get(group_by, "unknown"))].append(evaluation)
    return {key: summarize_scores(rows) for key, rows in sorted(groups.items())}


def dimension_summary(evaluations: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Summarize mean scores per rubric dimension name across all evaluations."""
    scores_by_dimension: dict[str, list[float]] = defaultdict(list)
    max_score_by_dimension: dict[str, float] = {}
    for evaluation in evaluations:
        for dimension in evaluation.get("dimension_scores", []):
            scores_by_dimension[dimension["name"]].append(float(dimension["score"]))
            max_score_by_dimension[dimension["name"]] = float(dimension["max_score"])

    summary: dict[str, dict[str, Any]] = {}
    for name, scores in sorted(scores_by_dimension.items()):
        max_score = max_score_by_dimension[name]
        summary[name] = {
            "count": len(scores),
            "mean_score": round(mean(scores), 4) if scores else 0.0,
            "max_score": max_score,
            "mean_normalized": round(mean(scores) / max_score, 4) if scores and max_score else 0.0,
        }
    return summary
