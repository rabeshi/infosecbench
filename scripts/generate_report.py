#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from infosecbench.metrics import group_summary
from infosecbench.reporting import export_group_summary_csv, render_markdown_report


def _load_evaluations(evaluations_path: Path) -> list[dict]:
    evaluations = []
    with evaluations_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                evaluations.append(json.loads(line))
    return evaluations


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Phase 2 report from scored InfoSecBench evaluations")
    parser.add_argument("--evaluations", type=str, required=True, help="Path to evaluations.jsonl from score_results.py")
    parser.add_argument("--output", type=str, required=True, help="Output directory for the report")
    args = parser.parse_args()

    evaluations_path = Path(args.evaluations)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    evaluations = _load_evaluations(evaluations_path)
    if not evaluations:
        raise SystemExit(f"No evaluations found in {evaluations_path}")

    summary_path = output_dir / "summary.md"
    summary_path.write_text(render_markdown_report(evaluations), encoding="utf-8")

    category_csv_path = export_group_summary_csv(
        group_summary(evaluations, "category"), "category", output_dir / "category_summary.csv"
    )

    print(f"Evaluated {len(evaluations)} scenarios.")
    print(f"Wrote Markdown report to {summary_path}")
    print(f"Wrote category summary CSV to {category_csv_path}")


if __name__ == "__main__":
    main()
