from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ScenarioEvaluation:
    scenario_id: str
    category: str
    score: float = 0.0
    notes: str = ""
    passed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "category": self.category,
            "score": self.score,
            "notes": self.notes,
            "passed": self.passed,
        }


class SimpleEvaluator:
    """Phase 1 rule-based scoring placeholder for research workflows."""

    @staticmethod
    def score_response(response: str, expected_behavior: str) -> ScenarioEvaluation:
        text = (response or "").lower()
        target = (expected_behavior or "").lower()
        if not text:
            return ScenarioEvaluation(scenario_id="", category="", score=0.0, notes="empty response", passed=False)

        overlap = 1.0 if target in text else 0.5 if any(token in text for token in target.split()) else 0.0
        score = 3.0 if overlap >= 1.0 else 1.5 if overlap >= 0.5 else 0.0
        return ScenarioEvaluation(scenario_id="", category="", score=score, notes="heuristic content match", passed=score >= 1.5)
