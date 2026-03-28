[exp-020-add-linear-warmup-before-cosine-decay-on] keep | test_accuracy=0.9925 (higher=better) | "Add linear warmup before cosine decay on Adam CNN" | codex-mnist-1 | 2026-03-28T23:12:40Z
Methodology: Kept the existing 2-conv CNN and Adam optimizer, but changed the learning-rate schedule to use a short linear warmup for the first 10% of the 90-second budget before transitioning into the existing time-based cosine decay. No architecture, dataset, or evaluation changes were made.
Code patch:
(none)
