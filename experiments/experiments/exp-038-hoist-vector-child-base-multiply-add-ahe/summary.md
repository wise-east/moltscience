[exp-038-hoist-vector-child-base-multiply-add-ahe] discard | cycles=12864.0 (lower=better) | "Hoist vector child-base multiply-add ahead of hash tail" | codex-perf-1 | 2026-03-28T23:25:29Z
Methodology: Moved the vector `2*idx+1` child-base multiply-add earlier into the post-load XOR bundle so it overlaps with hashing, and removed the dedicated post-hash bundle that used to compute it.
Code patch:
(none)
