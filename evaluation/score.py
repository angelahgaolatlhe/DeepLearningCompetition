import argparse
import json
import os
import sys

import numpy as np


def load_predictions(path: str) -> np.ndarray:
    if path.endswith(".npy"):
        return np.load(path)
    return np.loadtxt(path, dtype=int)


def extract_team_name(submission_path: str) -> str:
    if not submission_path:
        return os.environ.get("TEAM_NAME", "inconnu")
    base = os.path.basename(submission_path)
    if base.endswith(".enc"):
        return base[:-4]
    return os.path.splitext(base)[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--submission", default="")
    parser.add_argument("--output", default="results.json")
    args = parser.parse_args()

    test_labels_path = os.environ.get("TEST_LABELS_PATH", "evaluation/test_labels.npy")
    if not os.path.exists(test_labels_path):
        print("Erreur : fichier de labels de test introuvable")
        sys.exit(1)

    preds = load_predictions(args.predictions)
    y_true = np.load(test_labels_path)

    if len(preds) != len(y_true):
        print("Erreur : le nombre de prédictions ne correspond pas")
        sys.exit(1)

    accuracy = float(np.mean(preds == y_true))
    team = extract_team_name(args.submission)

    with open(args.output, "w") as f:
        json.dump({"accuracy": accuracy, "team": team}, f)
    print(f"Accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    main()
