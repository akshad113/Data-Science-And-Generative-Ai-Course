from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class SalesRow:
    order_id: str
    order_date: datetime
    region: str
    product: str
    channel: str
    units: int
    revenue: float


def _parse_date(value: str) -> datetime:
    return datetime.strptime(value.strip(), "%Y-%m-%d")


def _parse_int(value: str) -> int:
    return int(value.strip())


def _parse_float(value: str) -> float:
    return float(value.strip())


def load_sales_data(path: Path) -> list[SalesRow]:
    if not path.exists():
        raise FileNotFoundError(f"Could not find data file: {path}")

    rows: list[SalesRow] = []
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for raw in reader:
            rows.append(
                SalesRow(
                    order_id=raw["order_id"].strip(),
                    order_date=_parse_date(raw["order_date"]),
                    region=raw["region"].strip(),
                    product=raw["product"].strip(),
                    channel=raw["channel"].strip(),
                    units=_parse_int(raw["units"]),
                    revenue=_parse_float(raw["revenue"]),
                )
            )

    return rows


def _best_item(items: dict[str, float]) -> tuple[str, float]:
    return max(items.items(), key=lambda item: item[1])


def _monthly_key(date_value: datetime) -> str:
    return date_value.strftime("%Y-%m")


def analyze_sales_data(rows: Iterable[SalesRow]) -> dict[str, object]:
    sales_rows = list(rows)
    if not sales_rows:
        raise ValueError("No sales data found.")

    revenue_by_region: dict[str, float] = defaultdict(float)
    revenue_by_product: dict[str, float] = defaultdict(float)
    revenue_by_channel: dict[str, float] = defaultdict(float)
    revenue_by_month: dict[str, float] = defaultdict(float)
    units_by_product: dict[str, int] = defaultdict(int)

    total_revenue = 0.0
    total_units = 0

    for row in sales_rows:
        total_revenue += row.revenue
        total_units += row.units
        revenue_by_region[row.region] += row.revenue
        revenue_by_product[row.product] += row.revenue
        revenue_by_channel[row.channel] += row.revenue
        revenue_by_month[_monthly_key(row.order_date)] += row.revenue
        units_by_product[row.product] += row.units

    sorted_months = dict(sorted(revenue_by_month.items()))
    sorted_regions = dict(sorted(revenue_by_region.items(), key=lambda item: item[1], reverse=True))
    sorted_products = dict(sorted(revenue_by_product.items(), key=lambda item: item[1], reverse=True))
    sorted_channels = dict(sorted(revenue_by_channel.items(), key=lambda item: item[1], reverse=True))

    best_month = _best_item(revenue_by_month)
    worst_month = min(revenue_by_month.items(), key=lambda item: item[1])
    best_region = _best_item(revenue_by_region)
    best_product = _best_item(revenue_by_product)

    return {
        "order_count": len(sales_rows),
        "total_revenue": round(total_revenue, 2),
        "total_units": total_units,
        "average_order_value": round(total_revenue / len(sales_rows), 2),
        "average_units_per_order": round(total_units / len(sales_rows), 2),
        "best_month": {"month": best_month[0], "revenue": round(best_month[1], 2)},
        "worst_month": {"month": worst_month[0], "revenue": round(worst_month[1], 2)},
        "top_region": {"name": best_region[0], "revenue": round(best_region[1], 2)},
        "top_product": {"name": best_product[0], "revenue": round(best_product[1], 2)},
        "revenue_by_month": {month: round(value, 2) for month, value in sorted_months.items()},
        "revenue_by_region": {region: round(value, 2) for region, value in sorted_regions.items()},
        "revenue_by_product": {product: round(value, 2) for product, value in sorted_products.items()},
        "revenue_by_channel": {channel: round(value, 2) for channel, value in sorted_channels.items()},
        "units_by_product": dict(sorted(units_by_product.items(), key=lambda item: item[1], reverse=True)),
    }
