 # Guide complet de participation et de soumission
 
 Ce guide décrit le parcours complet des participants, depuis l’inscription jusqu’à la soumission finale, avec les aspects techniques, les règles officielles, le fonctionnement du leaderboard, des exemples concrets, des bonnes pratiques et une FAQ.
 
## 1) Inscription et accès aux données

1. Rejoindre la compétition sur ce dépôt GitHub.
2. Télécharger les données depuis Kaggle:
   https://www.kaggle.com/competitions/deep-learning-spring-2025-project-1/data
3. Respecter les conditions d’utilisation des données Kaggle.
 
 ## 2) Structure du dépôt et prérequis techniques
 
 Structure principale:
 
 - `baseline/` : scripts d’entraînement et d’inférence
 - `evaluation/` : script de scoring
 - `encryption/` : chiffrement/déchiffrement des soumissions
 - `leaderboard/` : génération du classement
 - `.github/workflows/` : automatisations CI et évaluation
 
 Pré-requis:
 
 - Python 3.9 (aligné avec l’environnement d’évaluation)
 - Dépendances: `baseline/requirements.txt`
 
 Installation:
 
 ```bash
 pip install -r baseline/requirements.txt
 ```
 
## 3) Contraintes et règles officielles

Les règles officielles sont définies dans ce dépôt GitHub et dans la description de la compétition. Les points suivants doivent être considérés comme obligatoires:

- Respect des délais annoncés sur le dépôt.
- Interdiction de fuite de labels de test.
- Soumission au format demandé.
- Respect des conditions d’utilisation des données Kaggle.
 
## 4) Pipeline technique de participation
 
 ### 4.1 Entraîner un modèle
 
 Le script de base entraîne un modèle CNN simple:
 
 ```bash
 python baseline/train.py
 ```
 
 Le modèle est enregistré en `baseline_model.pth`.
 
 ### 4.2 Générer des prédictions
 
 Le script d’inférence lit les images de test depuis `../data/test` (par défaut) et génère un fichier `predictions.txt` avec un label par ligne.
 
 ```bash
 python baseline/predyct.py
 ```
 
 Format attendu:
 
 ```
 3
 0
 7
 ...
 ```
 
### 4.3 Préparer la soumission
 
 Les soumissions doivent être chiffrées au format `.enc` avec la clé publique fournie.
 
 ```bash
 pip install cryptography
 python encryption/encrypt.py --input predictions.txt --output submissions/TEAM_NAME.enc --public-key encryption/public_key.pem
 ```
 
### 4.4 Soumettre via Pull Request
 
 1. Créer une branche dédiée:
 
 ```bash
 git checkout -b submit/TEAM_NAME
 ```
 
 2. Ajouter uniquement le fichier `.enc`:
 
 ```bash
 mkdir -p submissions
 git add submissions/TEAM_NAME.enc
 git commit -m "Add encrypted submission"
 git push origin submit/TEAM_NAME
 ```
 
 3. Ouvrir une Pull Request vers `main`.
 
 L’évaluation automatique s’exécute via GitHub Actions.
 
## 5) Formats, langages et structure du code
 
- Format de soumission: **fichier `.enc`** produit par `encryption/encrypt.py`.
- Format de prédictions: `predictions.txt` avec **un entier par ligne**.
 - Langages acceptés pour le développement: **libres**, tant que le format final est respecté.
 - Structure du code: libre, mais la soumission finale doit toujours respecter le flux décrit.
 
## 6) Système de soumission sécurisé (PR + chiffrement)

Ce dépôt utilise une évaluation automatique basée sur GitHub Actions:

1. Côté participant
   - Générer `predictions.txt`.
   - Chiffrer avec la clé publique:

```bash
python encryption/encrypt.py --input predictions.txt --output submissions/TEAM_NAME.enc --public-key encryption/public_key.pem
```

2. Côté dépôt
   - La Pull Request déclenche le workflow.
   - La clé privée est stockée dans GitHub Secrets et n’est jamais exposée.
   - Le fichier `.enc` est déchiffré dans un environnement isolé.
   - Les labels de test restent privés.

## 7) Fonctionnement du leaderboard
 
 Le leaderboard est généré par le script `leaderboard/update_leaderboard.py` à partir d’un fichier `results.json` produit par le scoring.
 
- **Métrique principale**: accuracy (taux de classification correcte).
- **Classement**: tri décroissant par accuracy.
- **Mise à jour**: après exécution du workflow d’évaluation.
- **Interprétation**: un score plus élevé = meilleure performance. Les égalités sont départagées par l’ordre d’arrivée (timestamp).
 
 Exemple de ligne du leaderboard:
 
 ```
 team,accuracy,submitted_at
 TEAM_A,0.893000,2025-01-15T13:20:45Z
 ```
 
## 8) Bonnes pratiques
 
 - Vérifier le format final de `predictions.txt`.
 - Ne jamais inclure de labels de test dans le pipeline d’inférence.
 - Tester la génération de `.enc` localement avant PR.
 - Soumettre une seule version par PR pour simplifier la validation.
 - Nettoyer les fichiers temporaires et respecter `.gitignore`.
 
## 9) Erreurs courantes à éviter
 
 - Mauvais format (ligne vide, séparateurs incorrects).
 - Inclusion de fichiers non demandés dans la PR.
 - Soumission non chiffrée.
 - Erreurs de nommage (`TEAM_NAME.enc` incorrect).
 
## 10) FAQ
 
 **Q1: Dois-je être collaborateur pour soumettre?**  
 Non. Utilisez un fork et une Pull Request.
 
 **Q2: Puis-je soumettre en dehors de Python?**  
 Oui, si vous respectez le format final et fournissez un `.enc` valide.
 
 **Q3: Pourquoi la PR échoue?**  
 Vérifiez le format du fichier `.enc`, les logs GitHub Actions, et les dépendances.
 
 **Q4: Que faire en cas d’égalité de score?**  
 Le classement est ordonné par accuracy, puis par timestamp.
 
**Q5: Où vérifier les règles officielles?**  
Sur ce dépôt GitHub et dans l’annonce de la compétition.

**Q6: Utilisez-vous une méthode Google Form?**  
Non. La méthode officielle ici est la Pull Request avec chiffrement.
