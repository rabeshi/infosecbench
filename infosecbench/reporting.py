from __future__ import annotations

import csv
from pathlib import Path


def export_summary_csv(rows: list[dict], output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["scenario_id", "category", "score", "status"])
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "scenario_id": row.get("scenario_id", ""),
                "category": row.get("category", ""),
                "score": row.get("score", 0.0),
                "status": row.get("status", "unknown"),
            })
    return output
