# InfoSecBench

InfoSecBench is an independent benchmarking framework for evaluating the information security knowledge, reasoning, safety, governance, and adversarial robustness of large language models.

## Overview

This repository contains the first implementation of the Phase 1 benchmark foundation. It focuses on:

- loading and validating the benchmark CSV dataset,
- defining a minimal model interface,
- running benchmark scenarios through a mock or custom model,
- capturing raw model outputs in JSONL,
- and exposing a Python and CLI workflow for local experimentation.

## Dataset

The current dataset is stored at [infosecbench_v0.2_source_mapped_250.csv](infosecbench_v0.2_source_mapped_250.csv). It includes 250 scenarios across five categories and 25 subcategories.

Key fields supported by the dataset loader include:

- scenario_id
- benchmark_version
- category
- subcategory
- difficulty
- scenario
- evaluation_prompt
- expected_behavior
- authorization_context
- risk_level
- scoring_rubric
- max_score
- review_status
- source_type
- primary_source
- source_reference
- source_url
- source_version
- source_alignment_level
- evidence_basis
- ground_truth
- ground_truth_status
- source_validation_status
- source_validation_notes
- expert_review_status

## Installation

```bash
cd /path/to/infosecbench
python -m pip install -e .
```

## Usage

```bash
python scripts/run_benchmark.py --dataset infosecbench_v0.2_source_mapped_250.csv --output results
python scripts/score_results.py --input results/results.jsonl --output results/results.csv
```

## Python API

```python
from infosecbench.dataset import Dataset
from infosecbench.models.mock import MockModel
from infosecbench.runner import BenchmarkRunner

benchmark = Dataset.from_csv("infosecbench_v0.2_source_mapped_250.csv")
model = MockModel(name="mock-model", response_text="safe answer")
runner = BenchmarkRunner(model=model, output_dir="results")

for row in benchmark.rows[:5]:
    runner.run_single_scenario(
        scenario_id=row["scenario_id"],
        category=row["category"],
        prompt=row["evaluation_prompt"],
        expected_behavior=row["expected_behavior"],
    )
```

## Current Status

This is an initial Phase 1 implementation designed for reproducibility and extension. It intentionally does not claim expert validation or research-grade benchmarking beyond the engineering foundation on which the full project will be built.

## Roadmap

- Phase 1: dataset validation, benchmark runner, model adapters, mock model, tests
- Phase 2: category-specific evaluation rubrics and scoring workflows
- Phase 3: metrics, comparisons, confidence intervals, and reports
- Phase 4: advanced research extensions and multi-turn evaluation support

## Research Note

This project is intended to serve as an independent, transparent benchmark framework for academic research. It distinguishes between operational cybersecurity tooling and scenario-based LLM evaluation.
