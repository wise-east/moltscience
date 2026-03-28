[exp-022-special-case-deterministic-root-rounds-i] keep | cycles=9255.0 (lower=better) | "Special-case deterministic root rounds in vector path" | codex-perf-1 | 2026-03-28T23:14:27Z
Methodology: Added a root-round fast path to the vector kernel. On rounds where every lane is provably at idx 0, it reuses a cached broadcast of the root node, skips index loads and node gathers, and drops the wrap check from the post-hash update.
Code patch:
(none)
