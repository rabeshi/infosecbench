#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from infosecbench.dataset import Dataset
from infosecbench.evaluator import RubricEvaluator
from infosecbench.reporting import export_evaluations_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Score InfoSecBench JSONL results against their rubrics")
    parser.add_argument("--input", type=str, required=True, help="Path to results.jsonl from the benchmark runner")
    parser.add_argument("--output", type=str, required=True, help="Path to write scored evaluations.jsonl")
    parser.add_argument("--csv", type=str, default=None, help="Optional path to also write a flattened CSV")
    parser.add_argument(
        "--dataset", type=str, default=None,
        help="Optional dataset CSV to fill in missing rubric metadata by scenario_id",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    dataset_by_id = {}
    if args.dataset:
        dataset_by_id = {row["scenario_id"]: row for row in Dataset.from_csv(args.dataset)}

    evaluator = RubricEvaluator()
    evaluations = []

    with input_path.open("r", encoding="utf-8") as source:
        for line in source:
            if not line.strip():
                continue
            record = json.loads(line)
            row = {**dataset_by_id.get(record.get("scenario_id", ""), {}), **record}
            evaluation = evaluator.score_response(row, record.get("response", ""))
            evaluations.append(evaluation.to_dict())

    with output_path.open("w", encoding="utf-8") as handle:
        for evaluation in evaluations:
            handle.write(json.dumps(evaluation, ensure_ascii=False) + "\n")

    print(f"Scored {len(evaluations)} results. Evaluations written to {output_path}")

    if args.csv:
        csv_path = export_evaluations_csv(evaluations, args.csv)
        print(f"Wrote flattened CSV to {csv_path}")


if __name__ == "__main__":
    main()
