from __future__ import annotations

import re
from dataclasses import dataclass

_DIMENSION_PATTERN = re.compile(r"^(?P<name>[a-z0-9_]+)_(?P<min>\d+)_(?P<max>\d+)$")


class RubricParseError(ValueError):
    """Raised when a scoring_rubric string cannot be parsed."""


@dataclass(frozen=True)
class RubricDimension:
    name: str
    min_score: float
    max_score: float


def parse_scoring_rubric(rubric: str) -> list[RubricDimension]:
    """Parse a 'name_min_max;name_min_max;...' scoring_rubric string.

    Dataset rubrics look like 'technical_accuracy_0_3;control_relevance_0_3;calibration_0_3'.
    """
    rubric = (rubric or "").strip()
    if not rubric:
        raise RubricParseError("scoring_rubric is empty")

    dimensions: list[RubricDimension] = []
    for part in rubric.split(";"):
        part = part.strip()
        if not part:
            continue
        match = _DIMENSION_PATTERN.match(part)
        if not match:
            raise RubricParseError(f"Could not parse rubric dimension: '{part}'")
        dimensions.append(
            RubricDimension(
                name=match.group("name"),
                min_score=float(match.group("min")),
                max_score=float(match.group("max")),
            )
        )

    if not dimensions:
        raise RubricParseError(f"No rubric dimensions found in '{rubric}'")
    return dimensions
