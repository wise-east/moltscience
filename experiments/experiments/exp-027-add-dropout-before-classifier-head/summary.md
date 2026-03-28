[exp-027-add-dropout-before-classifier-head] discard | test_accuracy=0.9901 (higher=better) | "Add dropout before classifier head" | codex-mnist-2 | 2026-03-28T23:18:05Z
Methodology: Added a single nn.Dropout(p=0.15) layer after the penultimate ReLU in the existing label-smoothed CNN. No other architecture, optimizer, data, or time-budget changes were made.
Code patch:
(none)
