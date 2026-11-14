
from decision_evaluation import evaluate_decision

def test_correct_answer_decision():
    result = evaluate_decision(
        "answer",
        "Employees receive 20 paid leaves annually."
    )

    assert result["actual_decision"] == "answer"
    assert result["decision_correct"] is True

def test_correct_abstention_decision():
    result = evaluate_decision(
        "abstain",
        "I don't have enough information to answer this."
    )

    assert result["actual_decision"] == "abstain"
    assert result["decision_correct"] is True

def test_incorrect_abstention_decision():
    result = evaluate_decision(
        "answer",
        "I don't have enough information to answer this."
    )

    assert result["decision_correct"] is False