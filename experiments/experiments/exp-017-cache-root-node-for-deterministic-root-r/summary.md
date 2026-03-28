[exp-017-cache-root-node-for-deterministic-root-r] keep | cycles=10530.0 (lower=better) | "Cache root node for deterministic root rounds" | codex-perf-2 | 2026-03-28T23:10:27Z
Methodology: Preloaded the root node value once into scratch, broadcast it to a vector, and special-cased the deterministic root rounds in the SIMD loop to hash against the cached root instead of rebuilding gather addresses and issuing vector loads.
Code patch:
(none)
