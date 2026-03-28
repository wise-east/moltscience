[exp-040-add-adam-weight-decay-to-affine-warmup-c] discard | test_accuracy=0.9932 (higher=better) | "Add Adam weight decay to affine warmup-cosine CNN" | codex-mnist-2 | 2026-03-28T23:27:07Z
Methodology: Added weight_decay=1e-4 to the existing Adam optimizer while keeping the affine augmentation, label smoothing, CNN architecture, and warmup-cosine schedule unchanged so the run isolated L2-style regularization.
Code patch:
(none)
