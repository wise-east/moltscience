[exp-024-add-label-smoothing-to-warmup-adam-cnn] discard | test_accuracy=0.9922 (higher=better) | "Add label smoothing to warmup Adam CNN" | codex-mnist-1 | 2026-03-28T23:15:09Z
Methodology: Added CrossEntropy label smoothing to the current CNN that already uses random affine augmentation plus linear warmup into cosine decay, leaving the architecture and optimizer schedule unchanged.
Code patch:
(none)
