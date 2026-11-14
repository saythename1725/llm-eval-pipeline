
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

BASELINE_PATH = BASE_DIR / "reports" / "baseline_report.json"
CURRENT_PATH = BASE_DIR / "reports" / "evaluation_report.json"

# Allowed quality drop: 5 percentage points
# Allowed latency increase: 20%
QUALITY_THRESHOLDS = {
    "answer_accuracy": 0.05,
    "average_faithfulness": 0.05,
    "decision_accuracy": 0.05,
    "hit_rate_at_3": 0.05,
    "mrr": 0.05,
    "precision_at_3": 0.05
}

LATENCY_THRESHOLD = 0.20


def load_report(path):

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)["run_summary"]


def check_regression():

    if not BASELINE_PATH.exists():
        print("Baseline report not found!")
        return

    if not CURRENT_PATH.exists():
        print("Current evaluation report not found!")
        return

    baseline = load_report(BASELINE_PATH)
    current = load_report(CURRENT_PATH)

    regressions = []

    print("\n" + "=" * 60)
    print("REGRESSION CHECK")
    print("=" * 60)

    # Check quality metrics
    for metric, threshold in QUALITY_THRESHOLDS.items():

        baseline_score = baseline.get(metric)
        current_score = current.get(metric)

        if baseline_score is None or current_score is None:
            print(f"{metric}: SKIPPED (metric missing)")
            continue

        drop = baseline_score - current_score

        print(f"\nMetric: {metric}")
        print("Baseline:", baseline_score)
        print("Current:", current_score)
        print("Drop:", round(drop, 3))

        if drop > threshold:

            regressions.append({
                "metric": metric,
                "baseline": baseline_score,
                "current": current_score,
                "drop": round(drop, 3)
            })

            print("STATUS: REGRESSION DETECTED")

        else:
            print("STATUS: PASSED")

    # Check generation latency
    metric = "average_generation_latency_ms"

    baseline_latency = baseline.get(metric)
    current_latency = current.get(metric)

    if baseline_latency is not None and current_latency is not None:

        increase = (
            (current_latency - baseline_latency) / baseline_latency
            if baseline_latency > 0 else 0
        )

        print("\nMetric:", metric)
        print("Baseline:", baseline_latency, "ms")
        print("Current:", current_latency, "ms")
        print("Increase:", round(increase * 100, 2), "%")

        if increase > LATENCY_THRESHOLD:

            regressions.append({
                "metric": metric,
                "baseline": baseline_latency,
                "current": current_latency,
                "increase_percentage": round(increase * 100, 2)
            })

            print("STATUS: LATENCY REGRESSION DETECTED")

        else:
            print("STATUS: PASSED")

    else:
        print("\nLatency check skipped: metric missing.")

    # Final result
    print("\n" + "=" * 60)

    if regressions:
        print("REGRESSION DETECTED!")
        print("Number of failed metrics:", len(regressions))

        for regression in regressions:
            print(regression)

    else:
        print("ALL METRICS PASSED!")

    return regressions


if __name__ == "__main__":

    regressions = check_regression()

    if regressions is None:
        sys.exit(2)

    if regressions:
        print("\nBUILD FAILED: Regression detected!")
        sys.exit(1)

    print("\nBUILD PASSED: No regression detected!")
    sys.exit(0)
