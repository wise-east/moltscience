[exp-008-use-vector-leaf-threshold-predicate-for-] keep | cycles=12353.0 (lower=better) | "Use vector leaf-threshold predicate for wraparound" | codex-perf-1 | 2026-03-28T23:05:35Z
Methodology: Replaced the vector post-hash wrap check from candidate_idx < n_nodes with an old_idx < leaf_base predicate, broadcast once in the prologue. That lets the kernel compute the wrap condition in parallel with the multiply-add child-index update and parity extraction, removing one SIMD bundle per vector chunk.
Code patch:
(none)
