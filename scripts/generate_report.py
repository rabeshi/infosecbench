#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a basic summary report from JSONL benchmark results")
    parser.add_argument("--results", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()

    results_dir = Path(args.results)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    categories = {}
    for file in sorted(results_dir.glob("*.jsonl")):
        with file.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                total += 1
                record = json.loads(line)
                category = record.get("category", "unknown")
                categories[category] = categories.get(category, 0) + 1

    summary_path = output_dir / "summary.txt"
    summary_lines = [
        "InfoSecBench benchmark summary",
        f"Total records: {total}",
        "",
        "By category:",
    ]
    for key, value in sorted(categories.items()):
        summary_lines.append(f"- {key}: {value}")

    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print(f"Wrote summary to {summary_path}")


if __name__ == "__main__":
    main()
