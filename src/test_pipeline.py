
from rag import generate_answer


def test_rag_pipeline_returns_answer():
    question = "How many paid leaves do employees receive annually?"

    result = generate_answer(question)

    assert isinstance(result, dict)
    assert result["answer"].strip() != ""
    assert len(result["retrieved_chunks"]) > 0
    assert len(result["retrieved_sources"]) > 0
