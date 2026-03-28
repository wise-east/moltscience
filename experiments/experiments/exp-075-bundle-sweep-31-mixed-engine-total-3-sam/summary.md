[exp-075-bundle-sweep-31-mixed-engine-total-3-sam] discard | cycles=147732.0 (lower=better) | "Bundle sweep 31: mixed-engine total=3 same=3 forward-hash" | codex-perf-2 | 2026-03-28T19:39:32Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 3 total ops and 3 ops on one engine, with mixed-engine bundles. Kept the original hash stage order.
Code patch:
(none)
