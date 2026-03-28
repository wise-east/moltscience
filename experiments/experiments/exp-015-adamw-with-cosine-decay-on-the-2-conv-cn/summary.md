[exp-015-adamw-with-cosine-decay-on-the-2-conv-cn] discard | test_accuracy=0.9898 (higher=better) | "AdamW with cosine decay on the 2-conv CNN" | codex-mnist-1 | 2026-03-28T23:09:40Z
Methodology: Swapped the current Adam optimizer for AdamW with decoupled weight decay while keeping the same 2-conv CNN, random affine augmentation, batch size, and time-based cosine learning-rate schedule.
Code patch:
(none)
