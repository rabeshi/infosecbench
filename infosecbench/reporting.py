from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .evaluator import RubricEvaluator
from .metrics import dimension_summary, group_summary, summarize_scores


def export_evaluations_csv(evaluations: list[dict[str, Any]], output_path: str | Path) -> Path:
    """Flatten evaluation dicts (including per-dimension scores) into a CSV."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    max_dimensions = max((len(e.get("dimension_scores", [])) for e in evaluations), default=0)
    fieldnames = ["scenario_id", "category", "subcategory", "difficulty", "risk_level",
                  "total_score", "max_total_score", "normalized_score", "passed"]
    for i in range(1, max_dimensions + 1):
        fieldnames += [f"dimension_{i}_name", f"dimension_{i}_score", f"dimension_{i}_max_score"]

    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for evaluation in evaluations:
            row = {key: evaluation.get(key, "") for key in fieldnames if not key.startswith("dimension_")}
            for i, dimension in enumerate(evaluation.get("dimension_scores", []), start=1):
                row[f"dimension_{i}_name"] = dimension["name"]
                row[f"dimension_{i}_score"] = dimension["score"]
                row[f"dimension_{i}_max_score"] = dimension["max_score"]
            writer.writerow(row)
    return output


def export_group_summary_csv(summary: dict[str, dict[str, Any]], group_label: str, output_path: str | Path) -> Path:
    """Write a group_summary()-style dict (e.g. by category) to CSV."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [group_label, "count", "mean_normalized_score", "median_normalized_score",
                  "min_normalized_score", "max_normalized_score", "pass_rate"]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for key, stats in summary.items():
            writer.writerow({group_label: key, **stats})
    return output


def render_markdown_report(evaluations: list[dict[str, Any]]) -> str:
    """Render a human-readable Markdown summary report from evaluation dicts."""
    overall = summarize_scores(evaluations)
    by_category = group_summary(evaluations, "category")
    by_difficulty = group_summary(evaluations, "difficulty")
    by_risk_level = group_summary(evaluations, "risk_level")
    by_dimension = dimension_summary(evaluations)

    lines = ["# InfoSecBench Benchmark Report", ""]
    lines.append("## Overall")
    lines.append("")
    lines.append(f"- Scenarios evaluated: {overall['count']}")
    lines.append(f"- Mean normalized score: {overall['mean_normalized_score']}")
    lines.append(f"- Median normalized score: {overall['median_normalized_score']}")
    lines.append(f"- Pass rate (normalized score >= {RubricEvaluator.PASS_THRESHOLD}): {overall['pass_rate']}")
    lines.append("")

    def _table(title: str, summary: dict[str, dict[str, Any]], key_label: str) -> list[str]:
        rows = [f"## {title}", "", f"| {key_label} | count | mean | median | pass rate |",
                "| --- | --- | --- | --- | --- |"]
        for key, stats in summary.items():
            rows.append(
                f"| {key} | {stats['count']} | {stats['mean_normalized_score']} | "
                f"{stats['median_normalized_score']} | {stats['pass_rate']} |"
            )
        rows.append("")
        return rows

    lines += _table("By Category", by_category, "category")
    lines += _table("By Difficulty", by_difficulty, "difficulty")
    lines += _table("By Risk Level", by_risk_level, "risk_level")

    lines.append("## By Rubric Dimension")
    lines.append("")
    lines.append("| dimension | count | mean score | max score | mean normalized |")
    lines.append("| --- | --- | --- | --- | --- |")
    for name, stats in by_dimension.items():
        lines.append(
            f"| {name} | {stats['count']} | {stats['mean_score']} | "
            f"{stats['max_score']} | {stats['mean_normalized']} |"
        )
    lines.append("")

    lines.append(
        "_Scores are produced by the deterministic heuristic RubricEvaluator "
        "(lexical overlap + keyword heuristics), not expert or model-based "
        "judgment. See infosecbench/evaluator.py for scoring logic._"
    )
    return "\n".join(lines) + "\n"
