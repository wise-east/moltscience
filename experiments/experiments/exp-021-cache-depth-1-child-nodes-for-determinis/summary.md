[exp-021-cache-depth-1-child-nodes-for-determinis] keep | cycles=10277.0 (lower=better) | "Cache depth-1 child nodes for deterministic round-1 loads" | codex-perf-2 | 2026-03-28T23:13:19Z
Methodology: Added a vector fast path for rounds where every lane is known to be at depth 1. The kernel now preloads the two depth-1 child node values once, broadcasts them, and uses a vector select instead of recomputing addresses and issuing scattered loads on those rounds.
Code patch:
(none)
