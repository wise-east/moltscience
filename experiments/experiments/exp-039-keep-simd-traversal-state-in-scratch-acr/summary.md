[exp-039-keep-simd-traversal-state-in-scratch-acr] discard | cycles=11456.0 (lower=better) | "Keep SIMD traversal state in scratch across rounds" | codex-perf-2 | 2026-03-28T23:26:47Z
Methodology: Reordered the SIMD hot path to process each 8-lane batch across all rounds while keeping v_idx entirely in scratch. The kernel now loads values once per batch, updates indices only in scratch, and writes back only the final values instead of reloading and storing indices every round.
Code patch:
(none)
