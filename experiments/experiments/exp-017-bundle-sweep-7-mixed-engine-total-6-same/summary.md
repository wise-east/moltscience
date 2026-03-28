[exp-017-bundle-sweep-7-mixed-engine-total-6-same] discard | cycles=147732.0 (lower=better) | "Bundle sweep 7: mixed-engine total=6 same=3 forward-hash" | codex-perf-2 | 2026-03-28T19:38:03Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 6 total ops and 3 ops on one engine, with mixed-engine bundles. Kept the original hash stage order.
Code patch:
(none)
