from __future__ import annotations


def _format_currency(value: float) -> str:
    return f"${value:,.2f}"


def _format_mapping(title: str, mapping: dict[str, float]) -> str:
    lines = [f"## {title}", ""]
    for key, value in mapping.items():
        lines.append(f"- {key}: {_format_currency(value)}")
    lines.append("")
    return "\n".join(lines)


def build_markdown_report(summary: dict[str, object]) -> str:
    revenue_by_month = summary["revenue_by_month"]
    revenue_by_region = summary["revenue_by_region"]
    revenue_by_product = summary["revenue_by_product"]
    revenue_by_channel = summary["revenue_by_channel"]
    units_by_product = summary["units_by_product"]

    lines = [
        "# Sales Insights Report",
        "",
        "## Executive Summary",
        "",
        f"- Orders analyzed: {summary['order_count']}",
        f"- Total revenue: {_format_currency(summary['total_revenue'])}",
        f"- Average order value: {_format_currency(summary['average_order_value'])}",
        f"- Average units per order: {summary['average_units_per_order']}",
        f"- Top region: {summary['top_region']['name']} ({_format_currency(summary['top_region']['revenue'])})",
        f"- Top product: {summary['top_product']['name']} ({_format_currency(summary['top_product']['revenue'])})",
        f"- Best month: {summary['best_month']['month']} ({_format_currency(summary['best_month']['revenue'])})",
        f"- Slowest month: {summary['worst_month']['month']} ({_format_currency(summary['worst_month']['revenue'])})",
        "",
        "## Monthly Revenue",
        "",
    ]

    for month, value in revenue_by_month.items():
        lines.append(f"- {month}: {_format_currency(value)}")

    lines.extend(
        [
            "",
            *_format_mapping("Revenue by Region", revenue_by_region).splitlines(),
            *_format_mapping("Revenue by Product", revenue_by_product).splitlines(),
            *_format_mapping("Revenue by Channel", revenue_by_channel).splitlines(),
            "## Units by Product",
            "",
        ]
    )

    for product, units in units_by_product.items():
        lines.append(f"- {product}: {units}")

    lines.extend(
        [
            "",
            "## GenAI Prompt Idea",
            "",
            "Use the generated `genai_prompt.txt` file to ask an LLM for a polished business summary, insights, and next-step recommendations.",
            "",
        ]
    )

    return "\n".join(lines)


def build_genai_prompt(summary: dict[str, object]) -> str:
    return f"""You are a senior business analyst.

Analyze the sales performance summary below and produce:
1. Three key insights.
2. Two risks or anomalies worth investigating.
3. Three practical next actions for the sales team.

Use concise, executive-friendly language.

Sales summary:
- Orders analyzed: {summary['order_count']}
- Total revenue: {_format_currency(summary['total_revenue'])}
- Average order value: {_format_currency(summary['average_order_value'])}
- Average units per order: {summary['average_units_per_order']}
- Top region: {summary['top_region']['name']} ({_format_currency(summary['top_region']['revenue'])})
- Top product: {summary['top_product']['name']} ({_format_currency(summary['top_product']['revenue'])})
- Best month: {summary['best_month']['month']} ({_format_currency(summary['best_month']['revenue'])})
- Slowest month: {summary['worst_month']['month']} ({_format_currency(summary['worst_month']['revenue'])})

Revenue by month:
{chr(10).join(f"- {month}: {_format_currency(value)}" for month, value in summary['revenue_by_month'].items())}

Revenue by region:
{chr(10).join(f"- {region}: {_format_currency(value)}" for region, value in summary['revenue_by_region'].items())}

Revenue by product:
{chr(10).join(f"- {product}: {_format_currency(value)}" for product, value in summary['revenue_by_product'].items())}
"""
