[exp-005-wider-hidden-layer-and-larger-batch] keep | test_accuracy=0.9806 (higher=better) | "Wider hidden layer and larger batch" | codex-mnist-1 | 2026-03-28T18:45:24Z
Methodology: Increased the hidden width from 128 to 256 and doubled batch size to 128 to trade slightly larger capacity for faster batch throughput within the same 90-second wall-clock budget.
Code patch:
diff --git a/problems/tiny-mnist/train.py b/problems/tiny-mnist/train.py
index aaf0a27..2705c9a 100644
--- a/problems/tiny-mnist/train.py
+++ b/problems/tiny-mnist/train.py
@@ -14,8 +14,8 @@ TRAIN_BUDGET_SEC = 90
 class TinyNet(nn.Module):
     def __init__(self):
         super().__init__()
-        self.fc1 = nn.Linear(784, 128)
-        self.fc2 = nn.Linear(128, 10)
+        self.fc1 = nn.Linear(784, 256)
+        self.fc2 = nn.Linear(256, 10)
 
     def forward(self, x):
         x = x.view(-1, 784)
@@ -32,7 +32,7 @@ def train():
     ])
     train_set = datasets.MNIST("data", train=True, download=True, transform=transform)
     test_set = datasets.MNIST("data", train=False, transform=transform)
-    train_loader = torch.utils.data.DataLoader(train_set, batch_size=64, shuffle=True)
+    train_loader = torch.utils.data.DataLoader(train_set, batch_size=128, shuffle=True)
     test_loader = torch.utils.data.DataLoader(test_set, batch_size=1000)
 
     model = TinyNet()

