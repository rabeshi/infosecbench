import pytest

from infosecbench.rubric import RubricParseError, parse_scoring_rubric


def test_parse_scoring_rubric_parses_all_dimensions() -> None:
    dimensions = parse_scoring_rubric("technical_accuracy_0_3;control_relevance_0_3;calibration_0_3")
    assert [d.name for d in dimensions] == ["technical_accuracy", "control_relevance", "calibration"]
    assert all(d.min_score == 0.0 and d.max_score == 3.0 for d in dimensions)


def test_parse_scoring_rubric_rejects_empty_string() -> None:
    with pytest.raises(RubricParseError):
        parse_scoring_rubric("")


def test_parse_scoring_rubric_rejects_malformed_dimension() -> None:
    with pytest.raises(RubricParseError):
        parse_scoring_rubric("not_a_valid_rubric")
