
import ollama
import json

client = ollama.Client(host="http://127.0.0.1:11434")


def evaluate_faithfulness(question, context, answer):

    prompt = f"""
You are a faithfulness evaluator for a RAG system.

Your task is to check whether every factual claim
in the generated answer is supported by the provided context.

Question:
{question}

Retrieved context:
{context}

Generated answer:
{answer}

Instructions:
1. Break the answer into individual factual claims.
2. Check each claim against the retrieved context.
3. A claim is supported only if the context provides evidence for it.
4. Do not use outside knowledge.
5. Return only valid JSON.

Required JSON format:
{{
    "total_claims": 2,
    "supported_claims": 1,
    "unsupported_claims": [
        "Example unsupported claim"
    ],
    "faithfulness_score": 0.5,
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

    return result
