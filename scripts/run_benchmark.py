#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from infosecbench.dataset import Dataset
from infosecbench.models.local import DEFAULT_OLLAMA_ENDPOINT, LocalModel
from infosecbench.models.mock import MockModel
from infosecbench.runner import BenchmarkRunner


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the InfoSecBench benchmark")
    parser.add_argument("--dataset", type=str, default="infosecbench_v0.2_source_mapped_250.csv")
    parser.add_argument("--output", type=str, default="results")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--model-type", choices=["mock", "ollama"], default="mock")
    parser.add_argument(
        "--model-name", type=str, default="mock-model",
        help="Model name; the Ollama model tag (e.g. 'llama3') when --model-type=ollama",
    )
    parser.add_argument("--endpoint", type=str, default=DEFAULT_OLLAMA_ENDPOINT, help="Ollama server endpoint")
    parser.add_argument("--mock-response", type=str, default="safe and evidence-based recommendation")
    args = parser.parse_args()

    dataset = Dataset.from_csv(Path(args.dataset))
    if args.model_type == "ollama":
        model = LocalModel(name=args.model_name, model=args.model_name, endpoint=args.endpoint)
    else:
        model = MockModel(name=args.model_name, response_text=args.mock_response)
    runner = BenchmarkRunner(model=model, output_dir=args.output)

    rows = dataset.rows[: args.limit] if args.limit is not None else dataset.rows
    for row in rows:
        runner.run_single_scenario(
            scenario_id=row["scenario_id"],
            category=row["category"],
            subcategory=row.get("subcategory", ""),
            difficulty=row.get("difficulty", ""),
            risk_level=row.get("risk_level", ""),
            prompt=row["evaluation_prompt"],
            expected_behavior=row["expected_behavior"],
            ground_truth=row.get("ground_truth", ""),
            authorization_context=row.get("authorization_context", ""),
            scoring_rubric=row.get("scoring_rubric", ""),
            max_score=row.get("max_score", ""),
        )

    print(f"Completed {len(rows)} scenarios. Results written to {runner.output_path}")


if __name__ == "__main__":
    main()
