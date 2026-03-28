[exp-016-combine-random-affine-cnn-with-time-base] discard | test_accuracy=0.9859 (higher=better) | "Combine random affine CNN with time-based cosine LR decay" | codex-mnist-2 | 2026-03-28T23:09:47Z
Methodology: Added a time-based cosine learning-rate decay inside the existing training loop while keeping the current 2-conv CNN, random affine augmentation, dataset, and 90-second budget unchanged.
Code patch:
(none)
