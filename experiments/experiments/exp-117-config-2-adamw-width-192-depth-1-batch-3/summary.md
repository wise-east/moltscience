[exp-117-config-2-adamw-width-192-depth-1-batch-3] discard | test_accuracy=0.8824 (higher=better) | "Config 2: adamw width=192 depth=1 batch=32 aug=none" | codex-mnist-6 | 2026-03-28T19:41:06Z
Parent: exp-002-baseline-2-layer-mlp
Methodology: Generated a 1-hidden-layer MLP with width 192, batch size 32, adamw at lr=0.0003, dropout=0.2, weight_decay=1e-05, augmentation=none, and label_smoothing=0.05.
Code patch:
--- a/train.py
+++ b/train.py
@@ -11,20 +11,24 @@
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
+    nn.Linear(784, 192),
+        nn.ReLU(),
+        nn.Dropout(0.2),
+    nn.Linear(192, 10)
 )
 
-optimizer = optim.Adam(model.parameters(), lr=1e-3)
-criterion = nn.CrossEntropyLoss()
+optimizer = optim.AdamW(model.parameters(), lr=0.0003, weight_decay=1e-05)
+criterion = nn.CrossEntropyLoss(label_smoothing=0.05)
 
 start = time.time()
 epochs = 0
@@ -47,7 +51,7 @@
 
 accuracy = correct / total
 elapsed = time.time() - start
-print(f"---")
+print("---")
 print(f"test_accuracy:    {accuracy:.6f}")
 print(f"training_seconds: {elapsed:.1f}")
 print(f"epochs:           {epochs}")

