[exp-161-config-8-sgd-width-128-depth-3-batch-32-] discard | test_accuracy=0.1353 (higher=better) | "Config 8: sgd width=128 depth=3 batch=32 aug=rotation" | codex-mnist-4 | 2026-03-28T19:50:44Z
Parent: exp-002-baseline-2-layer-mlp
Methodology: Generated a 3-hidden-layer MLP with width 128, batch size 32, sgd at lr=0.0003, dropout=0.0, weight_decay=0.0001, augmentation=rotation, and label_smoothing=0.02.
Code patch:
--- a/train.py
+++ b/train.py
@@ -8,23 +8,34 @@
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
+train_loader = torch.utils.data.DataLoader(train_ds, batch_size=32, shuffle=True)
 test_loader = torch.utils.data.DataLoader(test_ds, batch_size=1000)
 
 model = nn.Sequential(
     nn.Flatten(),
-    nn.Linear(784, 256),
-    nn.ReLU(),
-    nn.Linear(256, 10)
+    nn.Linear(784, 128),
+        nn.ReLU(),
+        nn.Dropout(0.0),
+        nn.Linear(128, 128),
+        nn.ReLU(),
+        nn.Dropout(0.0),
+        nn.Linear(128, 128),
+        nn.ReLU(),
+        nn.Dropout(0.0),
+    nn.Linear(128, 10)
 )
 
-optimizer = optim.Adam(model.parameters(), lr=1e-3)
-criterion = nn.CrossEntropyLoss()
+optimizer = optim.SGD(model.parameters(), lr=0.0003, momentum=0.9, nesterov=True, weight_decay=0.0001)
+criterion = nn.CrossEntropyLoss(label_smoothing=0.02)
 
 start = time.time()
 epochs = 0
@@ -47,7 +58,7 @@
 
 accuracy = correct / total
 elapsed = time.time() - start
-print(f"---")
+print("---")
 print(f"test_accuracy:    {accuracy:.6f}")
 print(f"training_seconds: {elapsed:.1f}")
 print(f"epochs:           {epochs}")

