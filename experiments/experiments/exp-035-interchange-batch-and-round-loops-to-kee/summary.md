[exp-035-interchange-batch-and-round-loops-to-kee] discard | cycles=11424.0 (lower=better) | "Interchange batch and round loops to keep state in scratch" | codex-perf-2 | 2026-03-28T23:23:37Z
Methodology: Reordered build_kernel so each vector or scalar lane loads its input index/value once, runs all rounds from scratch-resident state, then stores once at the end. This removes repeated input-memory traffic per round without changing the hash or tree-walk logic.
Code patch:
(none)
