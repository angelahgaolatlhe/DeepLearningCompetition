import csv
import json
import os
import sys
from datetime import datetime, timezone


def load_results(path: str) -> dict:
    with open(path, "r") as f:
        data = json.load(f)
    if "team" not in data or "accuracy" not in data:
        raise ValueError("results.json incomplet")
    return data


def load_leaderboard(path: str) -> list:
    if not os.path.exists(path):
        return []
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            if "accuracy" in row:
                row["accuracy"] = float(row["accuracy"])
            rows.append(row)
        return rows


def save_leaderboard(path: str, rows: list):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["team", "accuracy", "submitted_at"])
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "team": row["team"],
                    "accuracy": f"{float(row['accuracy']):.6f}",
                    "submitted_at": row["submitted_at"],
                }
            )


def update_leaderboard(results_path: str, leaderboard_path: str):
    result = load_results(results_path)
    rows = load_leaderboard(leaderboard_path)
    rows.append(
        {
            "team": result["team"],
            "accuracy": float(result["accuracy"]),
            "submitted_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    rows.sort(key=lambda r: r["accuracy"], reverse=True)
    save_leaderboard(leaderboard_path, rows)


def main():
    if len(sys.argv) < 2:
        print("Utilisation : python leaderboard/update_leaderboard.py results.json")
        sys.exit(1)
    results_path = sys.argv[1]
    leaderboard_path = "leaderboard/leaderboard.csv"
    try:
        update_leaderboard(results_path, leaderboard_path)
    except Exception as exc:
        print(f"Erreur leaderboard: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
