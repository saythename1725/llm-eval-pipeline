
import json
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent

REPORT_PATH = BASE_DIR / "reports" / "evaluation_report.json"
BASELINE_PATH = BASE_DIR / "reports" / "baseline_report.json"


def save_baseline():

    if not REPORT_PATH.exists():
        print("Evaluation report not found. Run evaluate.py first.")
        return

    shutil.copy2(REPORT_PATH, BASELINE_PATH)

    print("Baseline saved successfully!")
    print("Location:", BASELINE_PATH)

    with open(BASELINE_PATH, "r", encoding="utf-8") as file:
        report = json.load(file)

    print("\nBaseline metrics:")
    for metric, value in report["run_summary"].items():
        print(metric, ":", value)


if __name__ == "__main__":
    save_baseline()
