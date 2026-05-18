# GenAI Data Insights Project

This is a small starter project that combines:

- basic data science analysis on a sales CSV file
- a markdown report generator
- a GenAI-ready prompt that can be sent to an LLM for business recommendations

## What it does

The project loads `data/sample_sales.csv`, calculates a few useful metrics, and writes:

- `output/sales_insights_report.md`
- `output/genai_prompt.txt`

## Project Structure

```text
genai_data_insights_project/
├── data/
│   └── sample_sales.csv
├── output/
├── src/
│   ├── data_insights.py
│   └── report_writer.py
├── main.py
└── README.md
```

## How to run

From the project folder:

```bash
python main.py
```

## GenAI idea

The data science part computes the facts. The GenAI part turns those facts into a polished executive summary and action plan.

You can later connect the generated prompt to an LLM API if you want the model to produce:

- business insights
- anomaly explanations
- next-step recommendations

## Good next upgrades

- add a real dataset
- create charts with `matplotlib`
- connect an LLM API for automatic summaries
- turn this into a Streamlit dashboard
