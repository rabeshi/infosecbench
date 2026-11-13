import csv
from pathlib import Path

import pytest

from infosecbench.dataset import Dataset, DatasetValidationError


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    csv_path = tmp_path / "sample.csv"
    fieldnames = [
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
    ]
    rows = [
        {
            "scenario_id": "ISB-001",
            "benchmark_version": "0.2-draft",
            "category": "Security Knowledge",
            "subcategory": "Cryptography",
            "difficulty": "beginner",
            "scenario": "Test scenario 1",
            "evaluation_prompt": "Prompt 1",
            "expected_behavior": "Behavior 1",
            "authorization_context": "organizational_defensive_context",
            "risk_level": "low",
            "scoring_rubric": "technical_accuracy_0_3;control_relevance_0_3",
            "max_score": "9",
            "review_status": "draft_source_mapped_unvalidated",
            "source_type": "original_synthetic",
            "primary_source": "NIST SP 800-53 Revision 5",
            "source_reference": "SC (System and Communications Protection)",
            "source_url": "https://example.com/source",
            "source_version": "Rev.5",
            "source_alignment_level": "family-level",
            "evidence_basis": "synthetic_scenario_topic_aligned_to_primary_source",
            "ground_truth": "Ground truth 1",
            "ground_truth_status": "draft_author_written_not_expert_validated",
            "source_validation_status": "provisional_topic_mapping",
            "source_validation_notes": "test",
            "expert_review_status": "pending",
        },
        {
            "scenario_id": "ISB-002",
            "benchmark_version": "0.2-draft",
            "category": "Security Knowledge",
            "subcategory": "Cryptography",
            "difficulty": "intermediate",
            "scenario": "Test scenario 2",
            "evaluation_prompt": "Prompt 2",
            "expected_behavior": "Behavior 2",
            "authorization_context": "organizational_defensive_context",
            "risk_level": "medium",
            "scoring_rubric": "technical_accuracy_0_3;control_relevance_0_3",
            "max_score": "9",
            "review_status": "draft_source_mapped_unvalidated",
            "source_type": "original_synthetic",
            "primary_source": "NIST SP 800-53 Revision 5",
            "source_reference": "SC (System and Communications Protection)",
            "source_url": "https://example.com/source",
            "source_version": "Rev.5",
            "source_alignment_level": "family-level",
            "evidence_basis": "synthetic_scenario_topic_aligned_to_primary_source",
            "ground_truth": "Ground truth 2",
            "ground_truth_status": "draft_author_written_not_expert_validated",
            "source_validation_status": "provisional_topic_mapping",
            "source_validation_notes": "test",
            "expert_review_status": "pending",
        },
    ]
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return csv_path


def test_dataset_loads_and_validates(sample_csv: Path) -> None:
    ds = Dataset.from_csv(sample_csv)
    assert len(ds.rows) == 2
    assert ds.scenario_ids == ["ISB-001", "ISB-002"]
    assert ds.version == "0.2-draft"


def test_dataset_rejects_duplicate_scenario_ids(tmp_path: Path) -> None:
    csv_path = tmp_path / "duplicate.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "scenario_id","benchmark_version","category","subcategory","difficulty","scenario","evaluation_prompt",
            "expected_behavior","authorization_context","risk_level","scoring_rubric","max_score","review_status",
            "source_type","primary_source","source_reference","source_url","source_version","source_alignment_level",
            "evidence_basis","ground_truth","ground_truth_status","source_validation_status","source_validation_notes","expert_review_status"
        ])
        writer.writerow(["ISB-001", "0.2-draft", "Security Knowledge", "Cryptography", "beginner", "A", "P", "E", "organizational_defensive_context", "low", "x", "9", "draft_source_mapped_unvalidated", "original_synthetic", "NIST", "SC", "https://example.com", "Rev.5", "family-level", "synthetic", "G", "draft_author_written_not_expert_validated", "provisional_topic_mapping", "note", "pending"])
        writer.writerow(["ISB-001", "0.2-draft", "Security Knowledge", "Cryptography", "beginner", "B", "P", "E", "organizational_defensive_context", "low", "x", "9", "draft_source_mapped_unvalidated", "original_synthetic", "NIST", "SC", "https://example.com", "Rev.5", "family-level", "synthetic", "G", "draft_author_written_not_expert_validated", "provisional_topic_mapping", "note", "pending"])

    with pytest.raises(DatasetValidationError):
        Dataset.from_csv(csv_path)


def test_dataset_allows_filtering(sample_csv: Path) -> None:
    ds = Dataset.from_csv(sample_csv)
    filtered = ds.filter(category="Security Knowledge")
    assert len(filtered.rows) == 2
    assert filtered.rows[0]["scenario_id"] == "ISB-001"
