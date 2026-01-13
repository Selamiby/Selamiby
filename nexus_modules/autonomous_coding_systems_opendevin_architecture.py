import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import json

class OpenDevinDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

class OpenDevinModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(OpenDevinModel, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, output_dim)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

def train(model, device, loader, optimizer, criterion):
    model.train()
    total_loss = 0
    for batch_idx, (data, target) in enumerate(loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)

def test(model, device, loader, criterion):
    model.eval()
    total_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss = criterion(output, target)
            total_loss += loss.item()
            _, predicted = torch.max(output, 1)
            correct += (predicted == target).sum().item()

    accuracy = correct / len(loader.dataset)
    return total_loss / len(loader), accuracy

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    data = np.random.rand(100, 10)
    labels = np.random.randint(0, 2, 100)
    dataset = OpenDevinDataset(data, labels)
    loader = DataLoader(dataset, batch_size=10, shuffle=True)
    model = OpenDevinModel(10, 2)
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    for epoch in range(10):
        loss = train(model, device, loader, optimizer, criterion)
        test_loss, accuracy = test(model, device, loader, criterion)
        print(f"Epoch {epoch+1}, Loss: {loss:.4f}, Test Loss: {test_loss:.4f}, Accuracy: {accuracy:.4f}")

# NEXUS-ONE CORE MODULE