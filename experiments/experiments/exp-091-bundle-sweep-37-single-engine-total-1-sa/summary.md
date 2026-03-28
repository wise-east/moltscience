[exp-091-bundle-sweep-37-single-engine-total-1-sa] discard | cycles=147732.0 (lower=better) | "Bundle sweep 37: single-engine total=1 same=1 forward-hash" | codex-perf-2 | 2026-03-28T19:40:04Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 1 total ops and 1 ops on one engine, with single-engine bundles. Kept the original hash stage order.
Code patch:
(none)
