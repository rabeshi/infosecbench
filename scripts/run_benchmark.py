#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from infosecbench.dataset import Dataset
from infosecbench.models.mock import MockModel
from infosecbench.runner import BenchmarkRunner


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the InfoSecBench benchmark")
    parser.add_argument("--dataset", type=str, default="infosecbench_v0.2_source_mapped_250.csv")
    parser.add_argument("--output", type=str, default="results")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--model", type=str, default="mock")
    args = parser.parse_args()

    dataset = Dataset.from_csv(Path(args.dataset))
    model = MockModel(name=args.model, response_text="safe and evidence-based recommendation")
    runner = BenchmarkRunner(model=model, output_dir=args.output)

    rows = dataset.rows[: args.limit] if args.limit is not None else dataset.rows
    for row in rows:
        runner.run_single_scenario(
            scenario_id=row["scenario_id"],
            category=row["category"],
            prompt=row["evaluation_prompt"],
            expected_behavior=row["expected_behavior"],
        )

    print(f"Completed {len(rows)} scenarios. Results written to {runner.output_path}")


if __name__ == "__main__":
    main()
