"""
Tiny MNIST classifier. Agent modifies this file.
Fixed budget: 90 seconds of training on CPU.
Metric: test accuracy (higher is better).
"""
import time

import torch
import torch.nn as nn

TRAIN_BUDGET_SEC = 90


class TinyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 10)

    def forward(self, x):
        x = x.view(-1, 784)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)


def train():
    from torchvision import datasets, transforms

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ])
    train_set = datasets.MNIST("data", train=True, download=True, transform=transform)
    test_set = datasets.MNIST("data", train=False, transform=transform)
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=128, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=1000)

    model = TinyNet()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    start = time.time()
    epoch = 0
    while time.time() - start < TRAIN_BUDGET_SEC:
        model.train()
        for batch_x, batch_y in train_loader:
            if time.time() - start >= TRAIN_BUDGET_SEC:
                break
            optimizer.zero_grad()
            loss = criterion(model(batch_x), batch_y)
            loss.backward()
            optimizer.step()
        epoch += 1

    model.eval()
    correct = total = 0
    with torch.no_grad():
        for batch_x, batch_y in test_loader:
            pred = model(batch_x).argmax(dim=1)
            correct += (pred == batch_y).sum().item()
            total += batch_y.size(0)

    accuracy = correct / total
    elapsed = time.time() - start
    print("---")
    print(f"test_accuracy:    {accuracy:.6f}")
    print(f"training_seconds: {elapsed:.1f}")
    print(f"epochs:           {epoch}")
    print(f"num_params:       {sum(p.numel() for p in model.parameters())}")


if __name__ == "__main__":
    train()
