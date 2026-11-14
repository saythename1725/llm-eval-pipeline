
import ollama
import json

client = ollama.Client(host="http://127.0.0.1:11434")


def evaluate_answer(question, expected_answer, actual_answer):

    prompt = f"""
You are an evaluator for a RAG application.

Evaluate whether the actual answer correctly answers the question.

Question:
{question}

Expected answer:
{expected_answer}

Actual answer:
{actual_answer}

Rules:
1. Accept answers that have the same meaning, even if wording differs.
2. Mark answers incorrect if important facts or numbers are wrong.
3. Do not reward answers that contradict the expected answer.
4. Return only valid JSON.

Required JSON format:
{{
    "correct": true,
    "reason": "Brief explanation"
}}
"""

    response = client.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format="json"
    )

    result = json.loads(response.message.content)

    return {
        "correct": result["correct"],
        "reason": result["reason"],
        "method": "local_llm_judge"
    }
