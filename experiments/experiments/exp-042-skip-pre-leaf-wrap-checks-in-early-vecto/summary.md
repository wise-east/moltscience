[exp-042-skip-pre-leaf-wrap-checks-in-early-vecto] discard | cycles=12224.0 (lower=better) | "Skip pre-leaf wrap checks in early vector rounds" | codex-perf-1 | 2026-03-28T23:27:44Z
Methodology: Split the round loop into pre-wrap and wrap-required phases using forest_height. In rounds before the traversal can fall past the leaves, the kernel now omits the vector and scalar idx<n_nodes wrap checks and their select instructions, keeping the existing path for later rounds.
Code patch:
(none)
