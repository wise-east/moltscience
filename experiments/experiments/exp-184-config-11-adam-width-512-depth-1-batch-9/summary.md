[exp-184-config-11-adam-width-512-depth-1-batch-9] discard | test_accuracy=0.9101 (higher=better) | "Config 11: adam width=512 depth=1 batch=96 aug=rotation" | codex-mnist-4 | 2026-03-28T19:55:32Z
Parent: exp-002-baseline-2-layer-mlp
Methodology: Generated a 1-hidden-layer MLP with width 512, batch size 96, adam at lr=0.001, dropout=0.3, weight_decay=1e-05, augmentation=rotation, and label_smoothing=0.0.
Code patch:
--- a/train.py
+++ b/train.py
@@ -8,23 +8,28 @@
 TRAIN_BUDGET_SEC = 90
 
 transform = transforms.Compose([
+    transforms.RandomRotation(12),
     transforms.ToTensor(),
     transforms.Normalize((0.1307,), (0.3081,))
 ])
-train_ds = datasets.MNIST("data", train=True, download=True, transform=transform)
-test_ds = datasets.MNIST("data", train=False, transform=transform)
-train_loader = torch.utils.data.DataLoader(train_ds, batch_size=64, shuffle=True)
+train_ds = datasets.MNIST(r"/home/justin/ralphton/problems/tiny-mnist/data", train=True, download=True, transform=transform)
+test_ds = datasets.MNIST(r"/home/justin/ralphton/problems/tiny-mnist/data", train=False, transform=transforms.Compose([
+    transforms.ToTensor(),
+    transforms.Normalize((0.1307,), (0.3081,))
+]))
+train_loader = torch.utils.data.DataLoader(train_ds, batch_size=96, shuffle=True)
 test_loader = torch.utils.data.DataLoader(test_ds, batch_size=1000)
 
 model = nn.Sequential(
     nn.Flatten(),
-    nn.Linear(784, 256),
-    nn.ReLU(),
-    nn.Linear(256, 10)
+    nn.Linear(784, 512),
+        nn.ReLU(),
+        nn.Dropout(0.3),
+    nn.Linear(512, 10)
 )
 
-optimizer = optim.Adam(model.parameters(), lr=1e-3)
-criterion = nn.CrossEntropyLoss()
+optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-05)
+criterion = nn.CrossEntropyLoss(label_smoothing=0.0)
 
 start = time.time()
 epochs = 0
@@ -47,7 +52,7 @@
 
 accuracy = correct / total
 elapsed = time.time() - start
-print(f"---")
+print("---")
 print(f"test_accuracy:    {accuracy:.6f}")
 print(f"training_seconds: {elapsed:.1f}")
 print(f"epochs:           {epochs}")

