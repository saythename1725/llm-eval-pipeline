
from answer_evaluation import evaluate_answer

question = "How many paid leaves do employees receive annually?"

expected = "Full-time employees receive 20 paid leaves annually."

test_cases = [
    "Employees get 20 annual vacation days.",
    "Employees receive 30 paid leaves annually.",
    "The company provides 20 paid leaves every year."
]

for answer in test_cases:

    result = evaluate_answer(
        question,
        expected,
        answer
    )

    print("\nActual answer:", answer)
    print("Judge result:", result)
