[exp-034-cache-top-of-tree-node-values-for-determ] discard | cycles=12228.0 (lower=better) | "Cache top-of-tree node values for deterministic rounds" | codex-perf-1 | 2026-03-28T23:23:00Z
Methodology: Cached the root and its two children once in scratch, then special-cased vector rounds at deterministic depths 0 and 1 to replace per-lane node gather loads with broadcasts plus a register-level select.
Code patch:
(none)
