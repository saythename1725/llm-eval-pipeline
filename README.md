# LLM Evaluation Pipeline

A learning project for evaluating a retrieval-augmented generation (RAG) application. The pipeline answers company-policy questions using local Ollama models, measures retrieval and answer quality, generates reports, and checks for regressions in CI.

## What this project evaluates

- Retrieval quality using Precision@3, hit rate, and MRR
- Answer correctness using a local LLM judge
- Faithfulness of generated answers to retrieved context
- Whether the system answers or abstains when information is missing
- Generation and end-to-end evaluation latency
- Regressions against a saved baseline report

## Pipeline flow

```text
Policy documents
        |
        v
Chunking and embeddings
        |
        v
Persistent ChromaDB vector store
        |
        v
Question retrieval
        |
        v
RAG answer generation
        |
        v
Correctness, faithfulness, decision, retrieval, and latency evaluation
        |
        v
JSON report -> HTML report -> regression check
```

## Repository structure

```text
documents/                  Source company-policy documents
data/evaluation_dataset.json Evaluation questions and expected results
data/chroma_db/             Persistent ChromaDB vector store
src/ingestion.py            Document loading and chunking
src/vector_store.py         Embedding generation and ChromaDB indexing
src/retrieval.py            Vector search
src/rag.py                  RAG answer generation
src/answer_evaluation.py    LLM-based answer correctness judge
src/faithfulness_evaluation.py
                            LLM-based faithfulness judge
src/decision_evaluation.py  Answer-versus-abstain evaluation
src/evaluate.py             Main evaluation runner
src/generate_html_report.py HTML report generation
src/save_baseline.py        Save the current report as a baseline
src/regression_checker.py   Quality and latency regression checks
src/run_pipeline.py         Run the local pipeline end to end
src/test_*.py               Tests and evaluation examples
reports/                    JSON, HTML, and baseline reports
.github/workflows/          GitHub Actions workflow
```

## Requirements

- Python 3.11+
- Ollama
- The following Ollama models:

```text
qwen2.5:3b
nomic-embed-text
```

Install the Python packages:

```bash
pip install ollama chromadb langchain-text-splitters pytest
```

Start Ollama and download the models:

```bash
ollama serve
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

The code expects Ollama at `http://127.0.0.1:11434`.

## Run the pipeline

From the `src` directory:

```bash
cd src
python vector_store.py
python evaluate.py
python generate_html_report.py
python regression_checker.py
```

Or run the complete local pipeline:

```bash
cd src
python run_pipeline.py
```

The generated files are written to:

- `reports/evaluation_report.json`
- `reports/evaluation_report.html`

## Evaluation dataset

The dataset is stored in `data/evaluation_dataset.json`. Each example contains:

```json
{
  "id": "Q001",
  "question": "How many paid leaves do employees receive annually?",
  "expected_answer": "Full-time employees receive 20 paid leaves annually.",
  "expected_source": "leave_policy.txt",
  "expected_decision": "answer"
}
```

`expected_source` is `null` for questions where the system is expected to abstain.

## Baselines and regression checks

After running an evaluation, save it as the baseline with:

```bash
cd src
python save_baseline.py
```

The regression checker compares the current report with `reports/baseline_report.json`. It checks quality metrics such as answer accuracy, faithfulness, decision accuracy, retrieval metrics, and generation latency.

## Tests

Run the automated tests with:

```bash
cd src
python -m pytest -v
```

Some tests and evaluation examples use a live Ollama server. Make sure Ollama is running and the required models are available before running those files.

## Current scope and limitations

This project is designed for learning the fundamentals of RAG evaluation. The current metrics are intentionally simple:

- Retrieval relevance is evaluated primarily at the source-file level.
- The dataset is small and is not statistically representative.
- LLM-judge results can vary between runs.
- The faithfulness and correctness judges depend on the local model's interpretation.
- There is no token-cost tracking, confidence interval calculation, or percentile latency reporting yet.
- The pipeline currently focuses on one RAG application and one local model configuration.

These limitations make the project useful for understanding evaluation concepts, while leaving room for future work such as larger datasets, chunk-level relevance labels, citation evaluation, robustness tests, cost tracking, and statistically reliable regression analysis.
