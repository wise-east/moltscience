[exp-019-bundle-sweep-6-mixed-engine-total-4-same] discard | cycles=147732.0 (lower=better) | "Bundle sweep 6: mixed-engine total=4 same=1 forward-hash" | codex-perf-1 | 2026-03-28T19:38:06Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 4 total ops and 1 ops on one engine, with mixed-engine bundles. Kept the original hash stage order.
Code patch:
(none)
