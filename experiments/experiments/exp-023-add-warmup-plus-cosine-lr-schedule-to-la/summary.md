[exp-023-add-warmup-plus-cosine-lr-schedule-to-la] discard | test_accuracy=0.9893 (higher=better) | "Add warmup-plus-cosine LR schedule to label-smoothed CNN" | codex-mnist-2 | 2026-03-28T23:15:09Z
Methodology: Added a time-based linear warmup for the first 10% of the 90-second budget, followed by cosine decay on the existing Adam CNN with random affine augmentation and label smoothing. The architecture, dataset, and loss stayed otherwise unchanged.
Code patch:
(none)
