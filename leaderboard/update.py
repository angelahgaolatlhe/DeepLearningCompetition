import json
import os
import sys
from datetime import datetime

LEADERBOARD_FILE = 'leaderboard/README.md'
SCORES_FILE = 'scores.json'

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE) as f:
            return json.load(f)
    return []

def save_scores(scores):
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

def update_leaderboard(new_score, username):
    scores = load_scores()
    scores.append({'user': username, 'score': new_score, 'date': datetime.now().isoformat()})
    # Trier par score décroissant
    scores.sort(key=lambda x: x['score'], reverse=True)
    save_scores(scores)

    # Générer le tableau Markdown (top 20)
    lines = ['# Leaderboard\n', '| Rang | Participant | Score | Date |', '|------|-------------|-------|------|']
    for i, s in enumerate(scores[:20]):
        lines.append(f"| {i+1} | {s['user']} | {s['score']:.4f} | {s['date'][:10]} |")
    with open(LEADERBOARD_FILE, 'w') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Utilisation : python leaderboard/update.py score.json")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        score_data = json.load(f)
    username = os.environ.get('GITHUB_ACTOR', 'inconnu')
    update_leaderboard(score_data['accuracy'], username)
