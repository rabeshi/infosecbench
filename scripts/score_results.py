#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert benchmark JSONL results into CSV scores")
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open("r", encoding="utf-8") as source, output_path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=["scenario_id", "category", "response", "status"])
        writer.writeheader()
        for line in source:
            if not line.strip():
                continue
            item = json.loads(line)
            writer.writerow({
                "scenario_id": item.get("scenario_id", ""),
                "category": item.get("category", ""),
                "response": item.get("response", ""),
                "status": item.get("status", "unknown"),
            })

    print(f"Wrote scored results to {output_path}")


if __name__ == "__main__":
    main()
