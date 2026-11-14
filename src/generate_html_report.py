
import json
from pathlib import Path
from html import escape

BASE_DIR = Path(__file__).resolve().parent.parent

REPORT_PATH = BASE_DIR / "reports" / "evaluation_report.json"
HTML_PATH = BASE_DIR / "reports" / "evaluation_report.html"


def generate_html_report():

    with open(REPORT_PATH, "r", encoding="utf-8") as file:
        report = json.load(file)

    summary = report["run_summary"]

    metrics = [
        "answer_accuracy",
        "average_faithfulness",
        "decision_accuracy",
        "precision_at_3",
        "hit_rate_at_3",
        "mrr",
        "average_generation_latency_ms"
    ]

    metric_cards = ""

    for metric in metrics:
        value = summary.get(metric, "N/A")

        if isinstance(value, (int, float)):
            if metric.endswith("_ms"):
                display_value = f"{value:.2f} ms"
            else:
                display_value = f"{value:.2%}"
        else:
            display_value = str(value)

        metric_cards += f"""
        <div class="card">
            <p>{escape(metric.replace("_", " ").title())}</p>
            <h2>{escape(display_value)}</h2>
        </div>
        """

    # Find the per-question results list
    question_results = []

    for key, value in report.items():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            question_results = value
            break

    rows = ""

    for item in question_results:
        question = escape(str(item.get("question", "N/A")))
        answer = escape(str(item.get("actual_answer", "N/A")))

        rows += f"""
        <tr>
            <td>{escape(str(item.get("question_id", item.get("id", "N/A"))) )}</td>
            <td>{question}</td>
            <td>{answer}</td>
        </tr>
        """

    if not rows:
        rows = '<tr><td colspan="3">No per-question results found.</td></tr>'

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>LLM Evaluation Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f6f9;
                margin: 40px;
                color: #222;
            }}
            h1 {{ margin-bottom: 5px; }}
            .subtitle {{ color: #666; }}
            .metrics {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 30px;
            }}
            .card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 8px #ddd;
            }}
            .card p {{ color: #666; }}
            .card h2 {{ margin-bottom: 0; }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                margin-top: 20px;
            }}
            th, td {{
                padding: 14px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }}
            th {{ background: #e9edf3; }}
        </style>
    </head>

    <body>
        <h1>LLM Evaluation Report</h1>
        <p class="subtitle">RAG Evaluation & Regression Testing</p>

        <h2>Overall Metrics</h2>
        <div class="metrics">
            {metric_cards}
        </div>

        <h2>Individual Question Results</h2>
        <table>
            <tr>
                <th>Question ID</th>
                <th>Question</th>
                <th>Generated Answer</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

    HTML_PATH.write_text(html, encoding="utf-8")

    print("HTML report generated successfully!")
    print("Location:", HTML_PATH)


if __name__ == "__main__":
    generate_html_report()
