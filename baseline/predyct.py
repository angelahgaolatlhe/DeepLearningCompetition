import torch
import torchvision.transforms as transforms
from model import SimpleCNN
import numpy as np
import os
from PIL import Image

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
    images = sorted(os.listdir(test_dir))
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