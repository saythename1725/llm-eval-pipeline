
import subprocess
import sys

def run_step(step_name, command):

    print("\n" + "=" * 60)
    print("RUNNING:", step_name)
    print("=" * 60)

    result = subprocess.run(command)

    if result.returncode != 0:
        print(f"\nFAILED: {step_name}")
        sys.exit(result.returncode)

    print(f"\nPASSED: {step_name}")

if __name__ == "__main__":

    steps = [
        ("Build Vector Database", ["python", "vector_store.py"]),
        ("Run Unit and Integration Tests", [
            "python", "-m", "pytest",
            "test_decision_evaluation.py",
            "test_regression_checker.py",
            "test_pipeline.py",
            "-v"
        ]),
        ("Run LLM Evaluation", ["python", "evaluate.py"]),
        ("Generate HTML Report", ["python", "generate_html_report.py"]),
        ("Check Regressions", ["python", "regression_checker.py"])
    ]

    for step_name, command in steps:
        run_step(step_name, command)

    print("\n" + "=" * 60)
    print("COMPLETE PIPELINE PASSED!")
    print("=" * 60)