[exp-030-cache-deterministic-root-and-depth-1-vec] discard | cycles=12482.0 (lower=better) | "Cache deterministic root and depth-1 vector nodes" | codex-perf-1 | 2026-03-28T23:20:36Z
Methodology: Cached the first eight forest nodes into vector scratch once, then replaced the generic gather-based vector path for rounds 0 and 1 with deterministic root/depth-1 fast paths that use broadcasts and selects instead of per-lane forest gathers. Later rounds kept the existing generic vector traversal.
Code patch:
(none)
