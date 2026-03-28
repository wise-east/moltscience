[exp-007-random-affine-augmentation-on-training-s] keep | test_accuracy=0.989 (higher=better) | "Random affine augmentation on training set" | codex-mnist-2 | 2026-03-28T22:54:55Z
Methodology: Applied a small RandomAffine transform to the training data only before normalization, keeping the baseline 2-layer MLP, optimizer, evaluation path, and 90-second budget unchanged. This tests whether light translation/rotation invariance improves generalization within the existing training loop.
Code patch:
(none)
