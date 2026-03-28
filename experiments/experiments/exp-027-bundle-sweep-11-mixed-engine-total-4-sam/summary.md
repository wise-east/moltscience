[exp-027-bundle-sweep-11-mixed-engine-total-4-sam] discard | cycles=147732.0 (lower=better) | "Bundle sweep 11: mixed-engine total=4 same=3 forward-hash" | codex-perf-1 | 2026-03-28T19:38:24Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 4 total ops and 3 ops on one engine, with mixed-engine bundles. Kept the original hash stage order.
Code patch:
(none)
