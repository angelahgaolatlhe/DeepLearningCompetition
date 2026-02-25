# Train the simple CNN model
#imports
import os
import warnings
os.environ.setdefault("HF_HOME", "/tmp/hf-home")
os.environ.pop("TRANSFORMERS_CACHE", None)
warnings.filterwarnings("ignore", message="Using `TRANSFORMERS_CACHE` is deprecated.*", category=FutureWarning)
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.utils.hub")
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from model import SimpleCNN

def main():
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                            download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=64,
                                              shuffle=True, num_workers=2)
    model = SimpleCNN()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    num_classes = 10

    for epoch in range(10):
        running_loss = 0.0
        total = 0
        correct = 0
        cm = torch.zeros((num_classes, num_classes), dtype=torch.int64)
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
            indices = (labels * num_classes + preds).view(-1)
            cm += torch.bincount(indices.cpu(), minlength=num_classes * num_classes).reshape(num_classes, num_classes)
        eps = 1e-12
        tp = cm.diag().float()
        fp = cm.sum(0).float() - tp
        fn = cm.sum(1).float() - tp
        precision_per = tp / (tp + fp + eps)
        recall_per = tp / (tp + fn + eps)
        f1_per = 2 * precision_per * recall_per / (precision_per + recall_per + eps)
        accuracy = correct / max(total, 1)
        precision = precision_per.mean().item()
        recall = recall_per.mean().item()
        f1 = f1_per.mean().item()
        print(f'Epoch {epoch+1} loss: {running_loss/len(trainloader):.3f} accuracy: {accuracy:.3f} precision: {precision:.3f} recall: {recall:.3f} f1: {f1:.3f}')

    torch.save(model.state_dict(), 'baseline_model.pth')
    print('Entraînement terminé, modèle sauvegardé.')

if __name__ == '__main__':
    main()
