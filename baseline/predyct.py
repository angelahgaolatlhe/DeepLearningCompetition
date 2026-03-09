import torch
import torchvision.transforms as transforms
from model import SimpleCNN
import numpy as np
import os
from PIL import Image

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp"}
LABEL_EXTENSIONS = {".npy", ".npz", ".csv", ".txt"}


def list_image_files(test_dir):
    files = []
    for name in os.listdir(test_dir):
        path = os.path.join(test_dir, name)
        if not os.path.isfile(path):
            continue
        ext = os.path.splitext(name)[1].lower()
        if ext in IMAGE_EXTENSIONS:
            files.append(name)
    return sorted(files)


def find_label_files(test_dir):
    files = []
    for name in os.listdir(test_dir):
        path = os.path.join(test_dir, name)
        if not os.path.isfile(path):
            continue
        ext = os.path.splitext(name)[1].lower()
        if ext not in LABEL_EXTENSIONS:
            continue
        lower = name.lower()
        if "label" in lower or "labels" in lower:
            files.append(path)
    return files


def mask_labels_in_dir(test_dir):
    masked_dir = os.path.join("/tmp", "masked_labels")
    os.makedirs(masked_dir, exist_ok=True)
    masked_paths = []
    for path in find_label_files(test_dir):
        name = os.path.basename(path)
        ext = os.path.splitext(name)[1].lower()
        masked_path = os.path.join(masked_dir, name)
        try:
            if ext == ".npy":
                data = np.load(path)
                masked = np.full_like(data, np.nan, dtype=float)
                np.save(masked_path, masked)
            elif ext == ".npz":
                data = np.load(path)
                masked = {k: np.full_like(data[k], np.nan, dtype=float) for k in data.files}
                np.savez(masked_path, **masked)
            elif ext == ".csv":
                data = np.genfromtxt(path, delimiter=",")
                masked = np.full_like(np.atleast_1d(data), np.nan, dtype=float)
                np.savetxt(masked_path, masked, delimiter=",")
            else:
                data = np.genfromtxt(path)
                masked = np.full_like(np.atleast_1d(data), np.nan, dtype=float)
                np.savetxt(masked_path, masked)
        except Exception:
            with open(masked_path, "w") as f:
                f.write("nan\n")
        masked_paths.append(masked_path)
    return masked_paths


def main():
    # Chemin vers le dossier test (fourni par l'utilisateur)
    #Path of the test folder
    test_dir = '../data/test'   # à adapter
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = SimpleCNN()
    model.load_state_dict(torch.load('baseline_model.pth', map_location=device))
    model.to(device)
    model.eval()

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    # On suppose que les images de test sont nommées 0.png, 1.png, ... dans l'ordre
    # ou selon un fichier list.txt
    masked = mask_labels_in_dir(test_dir)
    if masked:
        print(f"Labels masqués: {len(masked)} fichier(s)")
    images = list_image_files(test_dir)
    if not images:
        print("Erreur : aucune image trouvée")
        return
    preds = []
    for img_name in images:
        img_path = os.path.join(test_dir, img_name)
        image = Image.open(img_path).convert('RGB')
        input_tensor = transform(image).unsqueeze(0).to(device)
        with torch.no_grad():
            output = model(input_tensor)
            pred = output.argmax(dim=1).item()
        preds.append(pred)

    # Sauvegarder les prédictions dans un fichier texte (une classe par ligne)
    # Save the predictionss in a text file
    np.savetxt('predictions.txt', np.array(preds), fmt='%d')
    print('Prédictions sauvegardées dans predictions.txt')

if __name__ == '__main__':
    main()
