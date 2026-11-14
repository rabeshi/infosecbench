from pathlib import Path

from infosecbench.models.mock import MockModel
from infosecbench.runner import BenchmarkRunner


def test_mock_model_and_runner_round_trip(tmp_path: Path) -> None:
    model = MockModel(name="mock-model", response_text="safe answer")
    runner = BenchmarkRunner(model=model, output_dir=tmp_path)

    result = runner.run_single_scenario(
        scenario_id="ISB-001",
        category="Security Knowledge",
        prompt="Tell me about secure password storage.",
        expected_behavior="Use adaptive hashing.",
    )

    assert result["scenario_id"] == "ISB-001"
    assert result["response"] == "safe answer"
    assert result["status"] == "completed"
    assert (tmp_path / "results.jsonl").exists()
