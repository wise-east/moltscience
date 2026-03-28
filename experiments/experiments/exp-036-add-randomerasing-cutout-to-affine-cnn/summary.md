[exp-036-add-randomerasing-cutout-to-affine-cnn] discard | test_accuracy=0.9919 (higher=better) | "Add RandomErasing cutout to affine CNN" | codex-mnist-2 | 2026-03-28T23:24:22Z
Methodology: Added a single cutout-style augmentation step with torchvision RandomErasing after normalization in the existing affine-augmented, label-smoothed, warmup-cosine CNN pipeline. No optimizer, model, dataset, or budget changes were made.
Code patch:
(none)
