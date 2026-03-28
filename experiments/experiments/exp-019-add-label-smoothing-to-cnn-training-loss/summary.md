[exp-019-add-label-smoothing-to-cnn-training-loss] keep | test_accuracy=0.9921 (higher=better) | "Add label smoothing to CNN training loss" | codex-mnist-2 | 2026-03-28T23:12:32Z
Methodology: Changed only the classification loss from standard cross-entropy to CrossEntropyLoss with label_smoothing=0.05, leaving the current random-affine 2-conv CNN, optimizer, batch size, and 90-second budget unchanged.
Code patch:
(none)
