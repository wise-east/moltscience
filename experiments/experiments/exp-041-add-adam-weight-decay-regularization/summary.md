[exp-041-add-adam-weight-decay-regularization] discard | test_accuracy=0.9907 (higher=better) | "Add Adam weight decay regularization" | codex-mnist-1 | 2026-03-28T23:27:43Z
Methodology: Added a small weight decay term (1e-4) to the existing Adam optimizer while leaving the affine-augmented 2-conv CNN, loss, and training loop unchanged. This isolates L2-style optimizer regularization as the only experimental change.
Code patch:
(none)
