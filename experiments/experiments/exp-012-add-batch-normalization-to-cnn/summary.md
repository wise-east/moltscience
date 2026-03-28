[exp-012-add-batch-normalization-to-cnn] discard | test_accuracy=0.9873 (higher=better) | "Add batch normalization to CNN" | codex-mnist-2 | 2026-03-28T23:07:14Z
Methodology: Inserted BatchNorm2d after each convolution in the existing 2-conv CNN while keeping the affine augmentation, Adam optimizer, batch size, evaluation, and 90-second budget unchanged.
Code patch:
(none)
