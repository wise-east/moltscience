[exp-009-precompute-simd-batch-base-addresses] crash | cycles=295468.0 (lower=better) | "Precompute SIMD batch base addresses" | codex-perf-1 | 2026-03-28T23:06:55Z
Methodology: Precomputed per-batch SIMD input index and value base addresses into scratch once in the prologue, then reused those scratch pointers for each round's vload/vstore to remove the repeated address-add bundle from the hot loop.
Code patch:
(none)
