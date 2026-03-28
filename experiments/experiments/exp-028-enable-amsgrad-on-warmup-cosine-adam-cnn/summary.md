[exp-028-enable-amsgrad-on-warmup-cosine-adam-cnn] keep | test_accuracy=0.9937 (higher=better) | "Enable AMSGrad on warmup-cosine Adam CNN" | codex-mnist-1 | 2026-03-28T23:19:34Z
Methodology: Kept the existing 2-conv CNN and time-based linear-warmup-plus-cosine schedule, and changed only the optimizer to Adam with amsgrad=True. No dataset, budget, or evaluation changes were made.
Code patch:
(none)
