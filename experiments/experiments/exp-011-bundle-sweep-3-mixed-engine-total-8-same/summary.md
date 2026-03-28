[exp-011-bundle-sweep-3-mixed-engine-total-8-same] discard | cycles=147732.0 (lower=better) | "Bundle sweep 3: mixed-engine total=8 same=1 forward-hash" | codex-perf-2 | 2026-03-28T19:37:52Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 8 total ops and 1 ops on one engine, with mixed-engine bundles. Kept the original hash stage order.
Code patch:
(none)
