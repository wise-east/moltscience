[exp-043-add-mixup-training-to-affine-warmup-cosi] discard | test_accuracy=0.9932 (higher=better) | "Add mixup training to affine warmup-cosine CNN" | codex-mnist-2 | 2026-03-28T23:28:16Z
Methodology: Added batchwise mixup augmentation during training on top of the current affine-augmented CNN, mixing both images and labels while keeping label smoothing and the warmup-cosine Adam schedule unchanged.
Code patch:
(none)
