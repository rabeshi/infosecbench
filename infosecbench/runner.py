from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models.base import BaseModel


class BenchmarkRunner:
    """A minimal benchmark execution engine for Phase 1."""

    def __init__(self, model: BaseModel, output_dir: str | Path = "results"):
        self.model = model
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.output_path = self.output_dir / "results.jsonl"

    def run_single_scenario(
        self,
        *,
        scenario_id: str,
        category: str,
        prompt: str,
        expected_behavior: str,
        subcategory: str = "",
        difficulty: str = "",
        risk_level: str = "",
        authorization_context: str = "",
        scoring_rubric: str = "",
        max_score: str = "",
        ground_truth: str = "",
        **kwargs: Any,
    ) -> dict[str, Any]:
        response = self.model.generate(prompt, **kwargs)
        record = {
            "scenario_id": scenario_id,
            "category": category,
            "subcategory": subcategory,
            "difficulty": difficulty,
            "risk_level": risk_level,
            "prompt": prompt,
            "expected_behavior": expected_behavior,
            "ground_truth": ground_truth,
            "authorization_context": authorization_context,
            "scoring_rubric": scoring_rubric,
            "max_score": max_score,
            "response": response,
            "status": "completed",
        }
        with self.output_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record
