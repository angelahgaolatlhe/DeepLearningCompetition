# Competition Baseline (CIFAR-10)

This repository provides a simple CNN baseline, a submission format, and an evaluation workflow for a CIFAR-10-style image classification competition.

## Repository Structure

- baseline/ : training and inference scripts for a simple CNN model
- evaluation/ : scoring script used by the evaluation workflow
- leaderboard/ : leaderboard update logic
- .github/workflows/ : automated evaluation on pull requests

## Requirements

Python 3.9 is used by the evaluation workflow.

Install dependencies:

```bash
pip install -r baseline/requirements.txt
```

## Train the Baseline Model

This downloads CIFAR-10 and trains a small CNN, then saves `baseline_model.pth`.

```bash
python baseline/train.py
```

The model file is saved in the current working directory.

## Generate Predictions

The prediction script expects test images in a folder, by default `../data/test` relative to `baseline/`, with filenames like `0.png`, `1.png`, ...

1. Update the test directory path in `baseline/predyct.py` if needed.
2. Run the script:

```bash
python baseline/predyct.py
```

This writes `predictions.txt` in the current working directory, with one class id per line.

## Submission Format

Submit a text file with one integer class id per line, ordered the same way as the test images. Example:

```
3
0
7
...
```

## Local Evaluation (Optional)

If you have the test labels locally, set `TEST_LABELS_PATH` to the `.npy` file and run:

```bash
python evaluation/score.py path/to/predictions.txt
```

This writes `score.json` with the accuracy.
# DeepLearningCompetition
