[exp-024-bundle-sweep-10-mixed-engine-total-8-sam] discard | cycles=147732.0 (lower=better) | "Bundle sweep 10: mixed-engine total=8 same=3 forward-hash" | codex-perf-2 | 2026-03-28T19:38:16Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 8 total ops and 3 ops on one engine, with mixed-engine bundles. Kept the original hash stage order.
Code patch:
(none)
