[exp-005-config-1-adamw-width-192-depth-3-batch-1] discard | test_accuracy=0.9712 (higher=better) | "Config 1: adamw width=192 depth=3 batch=128 aug=none" | smoke-mnist | 2026-03-28T19:37:13Z
Parent: exp-002-baseline-2-layer-mlp
Methodology: Generated a 3-hidden-layer MLP with width 192, batch size 128, adamw at lr=0.005, dropout=0.2, weight_decay=0.0005, augmentation=none, and label_smoothing=0.1.
Code patch:
--- a/train.py
+++ b/train.py
@@ -11,20 +11,30 @@
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
+train_loader = torch.utils.data.DataLoader(train_ds, batch_size=128, shuffle=True)
 test_loader = torch.utils.data.DataLoader(test_ds, batch_size=1000)
 
 model = nn.Sequential(
     nn.Flatten(),
-    nn.Linear(784, 256),
-    nn.ReLU(),
-    nn.Linear(256, 10)
+    nn.Linear(784, 192),
+        nn.ReLU(),
+        nn.Dropout(0.2),
+        nn.Linear(192, 192),
+        nn.ReLU(),
+        nn.Dropout(0.2),
+        nn.Linear(192, 192),
+        nn.ReLU(),
+        nn.Dropout(0.2),
+    nn.Linear(192, 10)
 )
 
-optimizer = optim.Adam(model.parameters(), lr=1e-3)
-criterion = nn.CrossEntropyLoss()
+optimizer = optim.AdamW(model.parameters(), lr=0.005, weight_decay=0.0005)
+criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
 
 start = time.time()
 epochs = 0
@@ -47,7 +57,7 @@
 
 accuracy = correct / total
 elapsed = time.time() - start
-print(f"---")
+print("---")
 print(f"test_accuracy:    {accuracy:.6f}")
 print(f"training_seconds: {elapsed:.1f}")
 print(f"epochs:           {epochs}")

