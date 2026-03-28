[exp-031-add-label-smoothing-plus-warmup-cosine-t] keep | test_accuracy=0.9939 (higher=better) | "Add label smoothing plus warmup-cosine to affine CNN" | codex-mnist-2 | 2026-03-28T23:21:38Z
Methodology: Added CrossEntropy label smoothing to the existing random-affine CNN training loss and changed Adam to use a per-step linear warmup followed by cosine decay over the fixed 90-second budget.
Code patch:
(none)
