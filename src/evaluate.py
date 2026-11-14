import json
import time
from pathlib import Path

from rag import generate_answer
from answer_evaluation import evaluate_answer
from faithfulness_evaluation import evaluate_faithfulness
from decision_evaluation import evaluate_decision


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "data" / "evaluation_dataset.json"
REPORT_PATH = BASE_DIR / "reports" / "evaluation_report.json"

TOP_K = 3


def run_evaluation():

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    evaluation_results = []

    for item in dataset:

        question = item["question"]
        expected_source = item["expected_source"]

        print("\n" + "=" * 60)
        print("Evaluating:", item["id"])
        print("Question:", question)

        # 1. Generate answer using RAG
        generation_start = time.perf_counter()

        result = generate_answer(question)

        generation_latency = (
            time.perf_counter() - generation_start
        ) * 1000

        retrieved_chunks = result["retrieved_chunks"]
        retrieved_sources = result["retrieved_sources"]

        retrieved_source_names = [
            source["source"] for source in retrieved_sources
        ]

        context = "\n\n".join(retrieved_chunks)

        # 2. Calculate retrieval metrics
        if expected_source is None:

            precision_at_k = None
            recall_at_k = None
            reciprocal_rank = None

        else:

            relevant_positions = [
                i + 1
                for i, source in enumerate(retrieved_source_names)
                if source == expected_source
            ]

            hits = len(relevant_positions)

            precision_at_k = (
                hits / len(retrieved_source_names)
                if retrieved_source_names else 0
            )

            # Source-level hit indicator, not true chunk-level recall.
            recall_at_k = 1.0 if hits > 0 else 0.0

            reciprocal_rank = (
                1 / relevant_positions[0]
                if relevant_positions else 0.0
            )

        # 3. Store retrieved chunk details
        chunk_details = []

        for i, chunk in enumerate(retrieved_chunks):

            source = retrieved_sources[i]["source"]

            relevant = (
                source == expected_source
                if expected_source is not None
                else None
            )

            chunk_details.append({
                "rank": i + 1,
                "source": source,
                "text": chunk,
                "relevant": relevant
            })

        # 4. Evaluate answer correctness
        correctness_start = time.perf_counter()

        correctness_result = evaluate_answer(
            question,
            item["expected_answer"],
            result["answer"]
        )

        correctness_latency = (
            time.perf_counter() - correctness_start
        ) * 1000

        # 5. Evaluate faithfulness
        faithfulness_start = time.perf_counter()

        faithfulness_result = evaluate_faithfulness(
            question,
            context,
            result["answer"]
        )

        faithfulness_latency = (
            time.perf_counter() - faithfulness_start
        ) * 1000

        # 6. Evaluate answer vs abstain decision
        decision_result = evaluate_decision(
            item["expected_decision"],
            result["answer"]
        )

        # 7. Calculate latency
        total_latency = (
            generation_latency
            + correctness_latency
            + faithfulness_latency
        )

        # 8. Print individual results
        print("\nGenerated answer:", result["answer"])
        print("Answer correct:", correctness_result["correct"])
        print(
            "Faithfulness:",
            faithfulness_result["faithfulness_score"]
        )
        print(
            "Decision correct:",
            decision_result["decision_correct"]
        )

        # 9. Store individual evaluation results
        evaluation_results.append({

            "id": item["id"],
            "question": question,

            "expected_answer": item["expected_answer"],
            "actual_answer": result["answer"],

            "expected_source": expected_source,
            "expected_decision": item["expected_decision"],

            "retrieved_chunks": chunk_details,

            "retrieval_metrics": {
                "precision_at_3": precision_at_k,
                "recall_at_3": recall_at_k,
                "reciprocal_rank": reciprocal_rank
            },

            "answer_evaluation": {
                "answer_correct": correctness_result["correct"],
                "judge_reason": correctness_result["reason"],
                "judge_method": correctness_result["method"]
            },

            "faithfulness_evaluation": faithfulness_result,

            "decision_evaluation": decision_result,

            "latency_ms": {
                "generation": round(generation_latency, 2),
                "correctness_judge": round(correctness_latency, 2),
                "faithfulness_judge": round(faithfulness_latency, 2),
                "total": round(total_latency, 2)
            }
        })

    # 10. Calculate overall retrieval metrics
    valid_results = [
        item for item in evaluation_results
        if item["retrieval_metrics"]["precision_at_3"] is not None
    ]

    if valid_results:

        average_precision = sum(
            item["retrieval_metrics"]["precision_at_3"]
            for item in valid_results
        ) / len(valid_results)

        average_mrr = sum(
            item["retrieval_metrics"]["reciprocal_rank"]
            for item in valid_results
        ) / len(valid_results)

        hit_rate = sum(
            item["retrieval_metrics"]["reciprocal_rank"] > 0
            for item in valid_results
        ) / len(valid_results)

    else:
        average_precision = 0
        average_mrr = 0
        hit_rate = 0

    # 11. Calculate answer accuracy
    correct_answers = sum(
        item["answer_evaluation"]["answer_correct"]
        for item in evaluation_results
    )

    answer_accuracy = (
        correct_answers / len(evaluation_results)
        if evaluation_results else 0
    )

    # 12. Calculate average faithfulness
    average_faithfulness = (
        sum(
            item["faithfulness_evaluation"]["faithfulness_score"]
            for item in evaluation_results
        ) / len(evaluation_results)
        if evaluation_results else 0
    )

    # 13. Calculate decision accuracy
    correct_decisions = sum(
        item["decision_evaluation"]["decision_correct"]
        for item in evaluation_results
    )

    decision_accuracy = (
        correct_decisions / len(evaluation_results)
        if evaluation_results else 0
    )

    # 14. Calculate average latency
    average_generation_latency = (
        sum(item["latency_ms"]["generation"] for item in evaluation_results)
        / len(evaluation_results)
        if evaluation_results else 0
    )

    average_total_latency = (
        sum(item["latency_ms"]["total"] for item in evaluation_results)
        / len(evaluation_results)
        if evaluation_results else 0
    )

    # 15. Create final JSON report
    final_report = {

        "run_summary": {

            "total_questions": len(dataset),

            "questions_with_relevant_source": len(valid_results),

            "precision_at_3": round(average_precision, 3),

            "hit_rate_at_3": round(hit_rate, 3),

            "mrr": round(average_mrr, 3),

            "answer_accuracy": round(answer_accuracy, 3),

            "average_faithfulness": round(average_faithfulness, 3),

            "decision_accuracy": round(decision_accuracy, 3),

            "correct_answers": correct_answers,

            "correct_decisions": correct_decisions,

            "average_generation_latency_ms": round(
                average_generation_latency, 2
            ),

            "average_total_latency_ms": round(
                average_total_latency, 2
            )
        },

        "results": evaluation_results
    }

    # 16. Save JSON report
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(REPORT_PATH, "w", encoding="utf-8") as file:

        json.dump(
            final_report,
            file,
            indent=4,
            ensure_ascii=False
        )

    # 17. Print final summary
    print("\n" + "=" * 60)
    print("FINAL EVALUATION SUMMARY")
    print("=" * 60)

    print("Total questions:", len(dataset))
    print("Precision@3:", round(average_precision, 3))
    print("Hit Rate@3:", round(hit_rate, 3))
    print("MRR:", round(average_mrr, 3))
    print("Answer accuracy:", round(answer_accuracy, 3))
    print("Average faithfulness:", round(average_faithfulness, 3))
    print("Decision accuracy:", round(decision_accuracy, 3))
    print(
        "Average generation latency:",
        round(average_generation_latency, 2),
        "ms"
    )

    print("\nEvaluation completed!")
    print("Report saved at:", REPORT_PATH)


if __name__ == "__main__":
    run_evaluation()
