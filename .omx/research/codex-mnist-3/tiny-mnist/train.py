import time

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms

TRAIN_BUDGET_SEC = 90

transform = transforms.Compose([
    transforms.RandomAffine(degrees=10, translate=(0.08, 0.08)),
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])
train_ds = datasets.MNIST(r"/home/justin/ralphton/problems/tiny-mnist/data", train=True, download=True, transform=transform)
test_ds = datasets.MNIST(r"/home/justin/ralphton/problems/tiny-mnist/data", train=False, transform=transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
]))
train_loader = torch.utils.data.DataLoader(train_ds, batch_size=256, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_ds, batch_size=1000)

model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(784, 128),
        nn.ReLU(),
        nn.Dropout(0.0),
        nn.Linear(128, 128),
        nn.ReLU(),
        nn.Dropout(0.0),
    nn.Linear(128, 10)
)

optimizer = optim.SGD(model.parameters(), lr=0.0008, momentum=0.9, nesterov=True, weight_decay=1e-05)
criterion = nn.CrossEntropyLoss(label_smoothing=0.05)

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
print("---")
print(f"test_accuracy:    {accuracy:.6f}")
print(f"training_seconds: {elapsed:.1f}")
print(f"epochs:           {epochs}")
print(f"num_params:       {sum(p.numel() for p in model.parameters())}")
