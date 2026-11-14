
from faithfulness_evaluation import evaluate_faithfulness

question = "How many paid leaves do employees receive?"

context = """
Every full-time employee receives 20 paid leaves annually.
Employees can carry forward a maximum of 5 unused leaves.
"""

test_answers = [
    "Employees receive 20 paid leaves annually.",
    "Employees receive 20 paid leaves annually and can carry forward 10 leaves.",
    "Employees receive 30 paid leaves annually."
]

for answer in test_answers:

    result = evaluate_faithfulness(
        question,
        context,
        answer
    )

    print("\nGenerated answer:", answer)
    print("Faithfulness evaluation:", result)
