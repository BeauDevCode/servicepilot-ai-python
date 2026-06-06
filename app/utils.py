import json
from datetime import date, datetime
from typing import Any


def money(value: float | int | None) -> str:
    return f"${float(value or 0):,.2f}"


def parse_line_items(raw: str | None) -> list[dict[str, Any]]:
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return []
    return parsed if isinstance(parsed, list) else []


def dumps_line_items(items: list[dict[str, Any]]) -> str:
    return json.dumps(items)


def human_date(value: datetime | date | None) -> str:
    if value is None:
        return "Unscheduled"
    return value.strftime("%b %d, %Y")


def split_lines(value: str | None) -> list[str]:
    if not value:
        return []
    return [line.strip("- ").strip() for line in value.splitlines() if line.strip()]

