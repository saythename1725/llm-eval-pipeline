
def evaluate_decision(expected_decision, actual_answer):

    abstention_message = (
        "i don't have enough information to answer this."
    )

    normalized_answer = actual_answer.lower().strip()

    actual_decision = (
        "abstain"
        if abstention_message in normalized_answer
        else "answer"
    )

    return {
        "expected_decision": expected_decision,
        "actual_decision": actual_decision,
        "decision_correct": (
            expected_decision == actual_decision
        )
    }
