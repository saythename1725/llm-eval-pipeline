
import json
import regression_checker


def create_report(path, metrics):
    """Create a temporary evaluation report."""
    report = {"run_summary": metrics}

    with open(path, "w", encoding="utf-8") as file:
        json.dump(report, file)


def test_no_regression(monkeypatch, tmp_path):
    baseline = {
        "answer_accuracy": 0.90,
        "average_faithfulness": 0.90,
        "decision_accuracy": 0.90,
        "hit_rate_at_3": 1.0,
        "mrr": 1.0,
        "precision_at_3": 0.90,
        "average_generation_latency_ms": 4000
    }

    current = baseline.copy()

    baseline_path = tmp_path / "baseline.json"
    current_path = tmp_path / "current.json"

    create_report(baseline_path, baseline)
    create_report(current_path, current)

    monkeypatch.setattr(
        regression_checker, "BASELINE_PATH", baseline_path
    )
    monkeypatch.setattr(
        regression_checker, "CURRENT_PATH", current_path
    )

    result = regression_checker.check_regression()

    assert result == []


def test_quality_regression_detected(monkeypatch, tmp_path):
    baseline = {
        "answer_accuracy": 0.90,
        "average_faithfulness": 0.90,
        "decision_accuracy": 0.90,
        "hit_rate_at_3": 1.0,
        "mrr": 1.0,
        "precision_at_3": 0.90,
        "average_generation_latency_ms": 4000
    }

    current = baseline.copy()
    current["answer_accuracy"] = 0.80

    baseline_path = tmp_path / "baseline.json"
    current_path = tmp_path / "current.json"

    create_report(baseline_path, baseline)
    create_report(current_path, current)

    monkeypatch.setattr(
        regression_checker, "BASELINE_PATH", baseline_path
    )
    monkeypatch.setattr(
        regression_checker, "CURRENT_PATH", current_path
    )

    result = regression_checker.check_regression()

    assert len(result) == 1
    assert result[0]["metric"] == "answer_accuracy"


def test_latency_regression_detected(monkeypatch, tmp_path):
    baseline = {
        "answer_accuracy": 0.90,
        "average_faithfulness": 0.90,
        "decision_accuracy": 0.90,
        "hit_rate_at_3": 1.0,
        "mrr": 1.0,
        "precision_at_3": 0.90,
        "average_generation_latency_ms": 4000
    }

    current = baseline.copy()
    current["average_generation_latency_ms"] = 5000

    baseline_path = tmp_path / "baseline.json"
    current_path = tmp_path / "current.json"

    create_report(baseline_path, baseline)
    create_report(current_path, current)

    monkeypatch.setattr(
        regression_checker, "BASELINE_PATH", baseline_path
    )
    monkeypatch.setattr(
        regression_checker, "CURRENT_PATH", current_path
    )

    result = regression_checker.check_regression()

    assert len(result) == 1
    assert result[0]["metric"] == "average_generation_latency_ms"


def test_missing_baseline_returns_none(monkeypatch, tmp_path):
    monkeypatch.setattr(
        regression_checker,
        "BASELINE_PATH",
        tmp_path / "missing.json"
    )

    result = regression_checker.check_regression()

    assert result is None
