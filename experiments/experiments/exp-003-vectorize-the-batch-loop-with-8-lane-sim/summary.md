[exp-003-vectorize-the-batch-loop-with-8-lane-sim] keep | cycles=14400.0 (lower=better) | "Vectorize the batch loop with 8-lane SIMD bundles" | codex-perf-1 | 2026-03-28T22:49:26Z
Methodology: Replaced the scalar per-item kernel with an 8-lane vector kernel that uses vload/vstore for contiguous batch data, vectorizes the hash and index-update math, and bundles independent ALU/load/store work into the same instruction cycles. Kept the required pause structure and a scalar tail path for non-multiple-of-8 batches.
Code patch:
(none)
