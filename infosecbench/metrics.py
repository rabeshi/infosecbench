from __future__ import annotations

from statistics import mean


def average(values: list[float]) -> float:
    return float(mean(values)) if values else 0.0


def summarize_scores(rows: list[dict]) -> dict[str, float]:
    scores = [float(row.get("score", 0.0)) for row in rows]
    return {
        "count": len(scores),
        "mean": average(scores),
        "median": float(sorted(scores)[len(scores) // 2]) if scores else 0.0,
        "min": min(scores) if scores else 0.0,
        "max": max(scores) if scores else 0.0,
    }
