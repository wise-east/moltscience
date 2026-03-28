[exp-171-config-9-sgd-width-256-depth-2-batch-32-] discard | test_accuracy=0.3299 (higher=better) | "Config 9: sgd width=256 depth=2 batch=32 aug=affine" | codex-mnist-2 | 2026-03-28T19:52:21Z
Parent: exp-002-baseline-2-layer-mlp
Methodology: Generated a 2-hidden-layer MLP with width 256, batch size 32, sgd at lr=0.0003, dropout=0.3, weight_decay=1e-05, augmentation=affine, and label_smoothing=0.0.
Code patch:
--- a/train.py
+++ b/train.py
@@ -8,23 +8,31 @@
 TRAIN_BUDGET_SEC = 90
 
 transform = transforms.Compose([
+    transforms.RandomAffine(degrees=10, translate=(0.08, 0.08)),
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
     nn.Linear(784, 256),
-    nn.ReLU(),
+        nn.ReLU(),
+        nn.Dropout(0.3),
+        nn.Linear(256, 256),
+        nn.ReLU(),
+        nn.Dropout(0.3),
     nn.Linear(256, 10)
 )
 
-optimizer = optim.Adam(model.parameters(), lr=1e-3)
-criterion = nn.CrossEntropyLoss()
+optimizer = optim.SGD(model.parameters(), lr=0.0003, momentum=0.9, nesterov=True, weight_decay=1e-05)
+criterion = nn.CrossEntropyLoss(label_smoothing=0.0)
 
 start = time.time()
 epochs = 0
@@ -47,7 +55,7 @@
 
 accuracy = correct / total
 elapsed = time.time() - start
-print(f"---")
+print("---")
 print(f"test_accuracy:    {accuracy:.6f}")
 print(f"training_seconds: {elapsed:.1f}")
 print(f"epochs:           {epochs}")

