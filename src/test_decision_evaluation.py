
from decision_evaluation import evaluate_decision

tests = [
    {
        "expected": "answer",
        "actual": "Employees receive 20 paid leaves annually."
    },
    {
        "expected": "abstain",
        "actual": "I don't have enough information to answer this."
    },
    {
        "expected": "abstain",
        "actual": "The company provides free meals."
    }
]

for test in tests:

    result = evaluate_decision(
        test["expected"],
        test["actual"]
    )

    print("\nExpected:", test["expected"])
    print("Actual answer:", test["actual"])
    print("Result:", result)
