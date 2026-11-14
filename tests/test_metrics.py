from infosecbench.metrics import dimension_summary, group_summary, summarize_scores


def _evaluation(scenario_id: str, category: str, normalized_score: float, passed: bool) -> dict:
    return {
        "scenario_id": scenario_id,
        "category": category,
        "difficulty": "beginner",
        "risk_level": "low",
        "dimension_scores": [
            {"name": "technical_accuracy", "score": normalized_score * 3, "max_score": 3},
        ],
        "total_score": normalized_score * 3,
        "max_total_score": 3,
        "normalized_score": normalized_score,
        "passed": passed,
    }


def test_summarize_scores_computes_aggregate_stats() -> None:
    evaluations = [
        _evaluation("ISB-001", "Security Knowledge", 1.0, True),
        _evaluation("ISB-002", "Security Knowledge", 0.0, False),
    ]

    summary = summarize_scores(evaluations)
    assert summary["count"] == 2
    assert summary["mean_normalized_score"] == 0.5
    assert summary["pass_rate"] == 0.5


def test_summarize_scores_handles_empty_list() -> None:
    summary = summarize_scores([])
    assert summary["count"] == 0
    assert summary["pass_rate"] == 0.0


def test_group_summary_groups_by_field() -> None:
    evaluations = [
        _evaluation("ISB-001", "Security Knowledge", 1.0, True),
        _evaluation("ISB-002", "Security Safety", 0.5, False),
    ]

    summary = group_summary(evaluations, "category")
    assert set(summary.keys()) == {"Security Knowledge", "Security Safety"}
    assert summary["Security Knowledge"]["mean_normalized_score"] == 1.0


def test_dimension_summary_aggregates_by_dimension_name() -> None:
    evaluations = [
        _evaluation("ISB-001", "Security Knowledge", 1.0, True),
        _evaluation("ISB-002", "Security Knowledge", 0.5, False),
    ]

    summary = dimension_summary(evaluations)
    assert summary["technical_accuracy"]["count"] == 2
    assert summary["technical_accuracy"]["mean_score"] == 2.25
