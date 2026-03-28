[exp-032-cache-first-two-tree-levels-for-vector-r] discard | cycles=12614.0 (lower=better) | "Cache first two tree levels for vector rounds 0 and 1" | codex-perf-2 | 2026-03-28T23:21:48Z
Methodology: Cached the root and depth-1 node values in scratch, broadcast them once, then special-cased vector round 0 and round 1 to replace the normal per-lane tree-node load sequence with the cached values and a vselect for left-vs-right child selection.
Code patch:
(none)
