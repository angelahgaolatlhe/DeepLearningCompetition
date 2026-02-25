# evaluation/score.py
import torch
import numpy as np
import json
import os
import sys

def main():
    # Le chemin du fichier de soumission est passé en argument
    # The path to the submission file is passed as an argument
    if len(sys.argv) < 2:
        print("Erreur : fichier de soumission manquant")
        sys.exit(1)
    submission_path = sys.argv[1]

    # Charger les prédictions du participant (format : un entier par ligne, ou un fichier .npy)
    # Ici on suppose un fichier texte avec une classe par ligne (dans l'ordre des images de test)
    # Load participant predictions (assuming a text file with one class per line)
    preds = np.loadtxt(submission_path, dtype=int)

    # Charger les vrais labels (récupérés depuis l'environnement ou un fichier temporaire)
    # On utilise une variable d'environnement pour le chemin
    # Use an environment variable for the path to the test labels file
    test_labels_path = os.environ.get('TEST_LABELS_PATH', 'evaluation/test_labels.npy')
    if not os.path.exists(test_labels_path):
        print("Erreur : fichier de labels de test introuvable")
        sys.exit(1)
    y_true = np.load(test_labels_path)

    if len(preds) != len(y_true):
        print("Erreur : le nombre de prédictions ne correspond pas")
        sys.exit(1)

    # Calculate accuracy
    accuracy = np.mean(preds == y_true)

    # Sauvegarder le score dans un fichier JSON pour l'étape suivante 
    # Save the score to a JSON file for the next step
    with open('score.json', 'w') as f:
        json.dump({'accuracy': accuracy}, f)
    print(f"Accuracy: {accuracy:.4f}")

if __name__ == '__main__':
    main()