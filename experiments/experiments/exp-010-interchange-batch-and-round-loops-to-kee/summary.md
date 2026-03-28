[exp-010-interchange-batch-and-round-loops-to-kee] keep | cycles=11424.0 (lower=better) | "Interchange batch and round loops to keep state in scratch" | codex-perf-2 | 2026-03-28T23:06:58Z
Methodology: Reordered the vector and scalar loops so each batch item is loaded once, processed through all rounds entirely in scratch, and stored back once at the end. This removes the per-round reload/store traffic while preserving semantics because batch lanes are independent.
Code patch:
(none)
