from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


class DatasetValidationError(ValueError):
    """Raised when a benchmark dataset is malformed."""


REQUIRED_COLUMNS = {
    "scenario_id",
    "benchmark_version",
    "category",
    "subcategory",
    "difficulty",
    "scenario",
    "evaluation_prompt",
    "expected_behavior",
    "authorization_context",
    "risk_level",
    "scoring_rubric",
    "max_score",
    "review_status",
    "source_type",
    "primary_source",
    "source_reference",
    "source_url",
    "source_version",
    "source_alignment_level",
    "evidence_basis",
    "ground_truth",
    "ground_truth_status",
    "source_validation_status",
    "source_validation_notes",
    "expert_review_status",
}


@dataclass
class Dataset:
    rows: list[dict[str, Any]]
    source_path: str = ""
    benchmark_version: str = ""

    @classmethod
    def from_csv(cls, path: str | Path) -> "Dataset":
        csv_path = Path(path)
        if not csv_path.exists():
            raise DatasetValidationError(f"Dataset file does not exist: {csv_path}")

        with csv_path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise DatasetValidationError(f"CSV file is missing a header row: {csv_path}")

            missing = sorted(REQUIRED_COLUMNS - set(reader.fieldnames))
            if missing:
                raise DatasetValidationError(
                    f"Dataset is missing required columns: {', '.join(missing)}"
                )

            rows = list(reader)

        if not rows:
            raise DatasetValidationError(f"Dataset is empty: {csv_path}")

        scenario_ids = [row.get("scenario_id", "") for row in rows]
        duplicates = sorted({value for value in scenario_ids if scenario_ids.count(value) > 1})
        if duplicates:
            raise DatasetValidationError(
                f"Duplicate scenario_id values found: {', '.join(duplicates)}"
            )

        for row in rows:
            for key in ("scenario_id", "benchmark_version", "category", "subcategory", "difficulty", "scenario"):
                if not str(row.get(key, "")).strip():
                    raise DatasetValidationError(f"Row contains a missing required value for '{key}'")

        version = rows[0].get("benchmark_version", "")
        return cls(rows=rows, source_path=str(csv_path), benchmark_version=str(version))

    @property
    def version(self) -> str:
        return self.benchmark_version

    @property
    def scenario_ids(self) -> list[str]:
        return [str(row["scenario_id"]) for row in self.rows]

    def filter(
        self,
        *,
        category: str | None = None,
        difficulty: str | None = None,
        risk_level: str | None = None,
        subcategory: str | None = None,
    ) -> "Dataset":
        filtered = self.rows
        if category is not None:
            filtered = [row for row in filtered if str(row.get("category", "")).lower() == str(category).lower()]
        if difficulty is not None:
            filtered = [row for row in filtered if str(row.get("difficulty", "")).lower() == str(difficulty).lower()]
        if risk_level is not None:
            filtered = [row for row in filtered if str(row.get("risk_level", "")).lower() == str(risk_level).lower()]
        if subcategory is not None:
            filtered = [row for row in filtered if str(row.get("subcategory", "")).lower() == str(subcategory).lower()]
        return Dataset(rows=filtered, source_path=self.source_path, benchmark_version=self.benchmark_version)

    def validation_summary(self) -> dict[str, Any]:
        categories = {}
        for row in self.rows:
            category = str(row.get("category", "unknown"))
            categories[category] = categories.get(category, 0) + 1

        return {
            "rows": len(self.rows),
            "benchmark_version": self.benchmark_version,
            "categories": categories,
            "scenario_ids_unique": len(self.scenario_ids) == len(set(self.scenario_ids)),
            "source_path": self.source_path,
        }

    def __len__(self) -> int:
        return len(self.rows)

    def __iter__(self):
        return iter(self.rows)
