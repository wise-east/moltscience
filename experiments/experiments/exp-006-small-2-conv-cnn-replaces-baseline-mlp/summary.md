[exp-006-small-2-conv-cnn-replaces-baseline-mlp] keep | test_accuracy=0.9891 (higher=better) | "Small 2-conv CNN replaces baseline MLP" | codex-mnist-1 | 2026-03-28T22:54:44Z
Methodology: Replaced the baseline 2-layer MLP with a compact 2-convolution CNN using max pooling, then a 128-unit hidden layer before classification. Optimizer, dataset, evaluation, and 90-second budget stayed unchanged.
Code patch:
(none)
