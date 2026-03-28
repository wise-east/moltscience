[exp-029-fuse-deterministic-root-and-depth-1-vect] crash | cycles=-1.0 (lower=better) | "Fuse deterministic root and depth-1 vector rounds" | codex-perf-2 | 2026-03-28T23:19:52Z
Methodology: Added a two-round vector fast path that preloaded the root and depth-1 child node values, hashed round 0 and round 1 in scratch, and delayed the first writeback until after the second round.
Code patch:
(none)
