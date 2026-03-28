[exp-011-time-based-cosine-decay-for-adam-on-the-] keep | test_accuracy=0.9915 (higher=better) | "Time-based cosine decay for Adam on the 2-conv CNN" | codex-mnist-1 | 2026-03-28T23:07:06Z
Methodology: Kept the current 2-conv CNN and random affine augmentation, but replaced the fixed Adam learning rate with a time-based cosine decay that starts at 2e-3 and anneals toward 1e-4 across the fixed 90-second training budget.
Code patch:
(none)
