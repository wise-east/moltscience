[exp-199-config-12-sgd-width-256-depth-2-batch-96] discard | test_accuracy=0.8865 (higher=better) | "Config 12: sgd width=256 depth=2 batch=96 aug=rotation" | codex-mnist-3 | 2026-03-28T19:57:08Z
Parent: exp-002-baseline-2-layer-mlp
Methodology: Generated a 2-hidden-layer MLP with width 256, batch size 96, sgd at lr=0.01, dropout=0.2, weight_decay=0.0, augmentation=rotation, and label_smoothing=0.1.
Code patch:
--- a/train.py
+++ b/train.py
@@ -8,23 +8,31 @@
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
     nn.Linear(784, 256),
-    nn.ReLU(),
+        nn.ReLU(),
+        nn.Dropout(0.2),
+        nn.Linear(256, 256),
+        nn.ReLU(),
+        nn.Dropout(0.2),
     nn.Linear(256, 10)
 )
 
-optimizer = optim.Adam(model.parameters(), lr=1e-3)
-criterion = nn.CrossEntropyLoss()
+optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9, nesterov=True, weight_decay=0.0)
+criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
 
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

