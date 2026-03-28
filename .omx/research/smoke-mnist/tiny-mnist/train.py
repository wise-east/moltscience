import time

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms

TRAIN_BUDGET_SEC = 90

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])
train_ds = datasets.MNIST("data", train=True, download=True, transform=transform)
test_ds = datasets.MNIST("data", train=False, transform=transform)
train_loader = torch.utils.data.DataLoader(train_ds, batch_size=64, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_ds, batch_size=1000)

model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Linear(256, 10)
)

optimizer = optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

start = time.time()
epochs = 0
while time.time() - start < TRAIN_BUDGET_SEC:
    model.train()
    for x, y in train_loader:
        if time.time() - start >= TRAIN_BUDGET_SEC:
            break
        optimizer.zero_grad()
        criterion(model(x), y).backward()
        optimizer.step()
    epochs += 1

model.eval()
correct = total = 0
with torch.no_grad():
    for x, y in test_loader:
        correct += (model(x).argmax(1) == y).sum().item()
        total += y.size(0)

accuracy = correct / total
elapsed = time.time() - start
print(f"---")
print(f"test_accuracy:    {accuracy:.6f}")
print(f"training_seconds: {elapsed:.1f}")
print(f"epochs:           {epochs}")
print(f"num_params:       {sum(p.numel() for p in model.parameters())}")
