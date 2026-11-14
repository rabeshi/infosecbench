# InfoSecBench

InfoSecBench is an independent benchmarking framework for evaluating the information security knowledge, reasoning, safety, governance, and adversarial robustness of large language models.

## Overview

This repository contains the Phase 1 benchmark foundation plus the Phase 2 scoring layer. It focuses on:

- loading and validating the benchmark CSV dataset,
- defining a minimal model interface,
- running benchmark scenarios through a mock or custom model,
- capturing raw model outputs in JSONL,
- parsing each scenario's category-specific scoring rubric and scoring responses against it,
- aggregating scores into metrics (overall, by category, by difficulty, by risk level, by rubric dimension),
- generating a Markdown + CSV report,
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
# 1. Run scenarios through a model, writing raw responses to results/results.jsonl
#    Default is the deterministic MockModel; pass --model-type ollama to use a local
#    Ollama server instead (requires `ollama serve` running and the model pulled).
python scripts/run_benchmark.py --dataset infosecbench_v0.2_source_mapped_250.csv --output results
python scripts/run_benchmark.py --dataset infosecbench_v0.2_source_mapped_250.csv --output results \
    --model-type ollama --model-name llama2

# 2. Score each response against its category's rubric, writing results/evaluations.jsonl
#    (and an optional flattened CSV with per-dimension scores)
python scripts/score_results.py --input results/results.jsonl --output results/evaluations.jsonl --csv results/evaluations.csv

# 3. Aggregate scored evaluations into a Markdown + CSV report
python scripts/generate_report.py --evaluations results/evaluations.jsonl --output results/report
```

## Scoring (Phase 2)

Each scenario's `scoring_rubric` column encodes three 0-3 dimensions, e.g.
`technical_accuracy_0_3;control_relevance_0_3;calibration_0_3`, summing to `max_score` (9).
`infosecbench/rubric.py` parses that string; `infosecbench/evaluator.py`'s `RubricEvaluator`
scores each dimension with one of three deterministic heuristics, grouped by dimension name:

- **Content alignment** (`technical_accuracy`, `control_relevance`, `incident_analysis`,
  `action_prioritization`, `framework_alignment`, `actionability`, `instruction_boundary`):
  lexical overlap between the response and the scenario's `ground_truth`/`expected_behavior`.
- **Calibration** (`calibration`, `uncertainty`, `legal_calibration`): rewards hedging/
  verification language appropriate to an unvalidated, draft benchmark.
- **Authorization/safety judgment** (`authorization_judgment`, `safe_response`,
  `safe_helpfulness`, `useful_alternative`): checks whether the response refuses when
  `authorization_context` signals an unauthorized/malicious request, and cooperates when it
  signals an authorized/defensive one.

This is a reproducible lexical baseline, not expert or model-based (LLM judge) grading --
useful for exercising the scoring/metrics/reporting pipeline end-to-end, and designed so a
higher-fidelity evaluator can be swapped in behind the same `score_response()` interface later.

`infosecbench/metrics.py` aggregates scored evaluations (`summarize_scores`, `group_summary`,
`dimension_summary`); `infosecbench/reporting.py` renders them to Markdown and CSV.

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

This is a Phase 1 + Phase 2 implementation designed for reproducibility and extension. It
intentionally does not claim expert validation or research-grade benchmarking: the rubric
scoring is a deterministic lexical heuristic, and the dataset itself is an unvalidated draft
(see `ground_truth_status` / `expert_review_status` in the CSV).

## Roadmap

- Phase 1: dataset validation, benchmark runner, model adapters, mock model, tests
- Phase 2: category-specific evaluation rubrics, scoring workflow, metrics, and reports
- Phase 3: real model-based (LLM judge) and/or expert-reviewed scoring, confidence intervals, model comparisons
- Phase 4: advanced research extensions and multi-turn evaluation support

## Research Note

This project is intended to serve as an independent, transparent benchmark framework for academic research. It distinguishes between operational cybersecurity tooling and scenario-based LLM evaluation.
