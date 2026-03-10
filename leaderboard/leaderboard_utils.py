import csv
from datetime import datetime, timedelta, timezone


def load_leaderboard(path: str) -> list:
    rows = []
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            accuracy = float(row.get("accuracy", "0") or 0)
            submitted_at = row.get("submitted_at", "")
            parsed_date = None
            if submitted_at:
                parsed_date = datetime.fromisoformat(submitted_at)
                if parsed_date.tzinfo is None:
                    parsed_date = parsed_date.replace(tzinfo=timezone.utc)
            rows.append(
                {
                    "team": row.get("team", ""),
                    "accuracy": accuracy,
                    "submitted_at": parsed_date,
                }
            )
    return rows


def sort_rows(rows: list, key: str = "accuracy", descending: bool = True) -> list:
    def sort_key(row):
        value = row.get(key)
        if key == "submitted_at":
            value = row.get("submitted_at") or datetime.min.replace(tzinfo=timezone.utc)
        return value
    return sorted(rows, key=sort_key, reverse=descending)


def filter_by_query(rows: list, query: str) -> list:
    if not query:
        return rows
    lowered = query.lower()
    return [row for row in rows if lowered in row.get("team", "").lower()]


def filter_by_period(rows: list, period: str) -> list:
    if period == "all":
        return rows
    now = datetime.now(timezone.utc)
    if period == "24h":
        cutoff = now - timedelta(hours=24)
    elif period == "7d":
        cutoff = now - timedelta(days=7)
    elif period == "30d":
        cutoff = now - timedelta(days=30)
    else:
        return rows
    filtered = []
    for row in rows:
        submitted_at = row.get("submitted_at")
        if submitted_at and submitted_at >= cutoff:
            filtered.append(row)
    return filtered
