[exp-026-derive-depth-1-vector-child-nodes-from-s] crash | cycles=-1.0 (lower=better) | "Derive depth-1 vector child nodes from stored parity" | codex-perf-1 | 2026-03-28T23:16:39Z
Methodology: Special-cased the deterministic round immediately after a root round by caching the depth-1 node values, deriving each lane's current index from the stored value parity, and skipping the usual vector index/node memory prefetches for that round.
Code patch:
(none)
