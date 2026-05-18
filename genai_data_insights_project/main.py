from pathlib import Path

from src.data_insights import analyze_sales_data, load_sales_data
from src.report_writer import build_genai_prompt, build_markdown_report


def main() -> None:
    project_root = Path(__file__).resolve().parent
    data_path = project_root / "data" / "sample_sales.csv"
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)

    sales_rows = load_sales_data(data_path)
    summary = analyze_sales_data(sales_rows)

    report_path = output_dir / "sales_insights_report.md"
    prompt_path = output_dir / "genai_prompt.txt"

    report_path.write_text(build_markdown_report(summary), encoding="utf-8")
    prompt_path.write_text(build_genai_prompt(summary), encoding="utf-8")

    print("Project created successfully.")
    print(f"Report written to: {report_path}")
    print(f"GenAI prompt written to: {prompt_path}")


if __name__ == "__main__":
    main()
