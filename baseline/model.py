import torch.nn as nn
import torch.nn.functional as F
# Simple CNN model for CIFAR-10
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        # First convolutional layer: 3 input channels (RGB), 32 output channels, 3x3 kernel
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        # Second convolutional layer: 32 input channels, 64 output channels, 3x3 kernel 
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        # Max pooling layer: 2x2 kernel
        self.pool = nn.MaxPool2d(2, 2)
        # First fully connected layer: 64*8*8 input features, 128 output features
        self.fc1 = nn.Linear(64 * 8 * 8, 128)
        self.dropout = nn.Dropout(0.5) #Dropout
        # Second fully connected layer: 128 input features, 10 output features (for 10 classes)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        # Apply first convolutional layer followed by ReLU activation and max pooling
        x = self.pool(F.relu(self.conv1(x)))
        # Apply second convolutional layer followed by ReLU activation and max pooling
        x = self.pool(F.relu(self.conv2(x)))
        # Flatten the tensor for the fully connected layer
        x = x.view(-1, 64 * 8 * 8)
        # Apply first fully connected layer followed by ReLU activation
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        # Apply second fully connected layer to get the output logits
        x = self.fc2(x)
        return x
