[exp-057-bundle-sweep-27-mixed-engine-total-1-sam] discard | cycles=147732.0 (lower=better) | "Bundle sweep 27: mixed-engine total=1 same=1 forward-hash" | codex-perf-2 | 2026-03-28T19:39:16Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 1 total ops and 1 ops on one engine, with mixed-engine bundles. Kept the original hash stage order.
Code patch:
(none)
