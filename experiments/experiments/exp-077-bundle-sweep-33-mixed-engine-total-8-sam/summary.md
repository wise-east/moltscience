[exp-077-bundle-sweep-33-mixed-engine-total-8-sam] discard | cycles=147732.0 (lower=better) | "Bundle sweep 33: mixed-engine total=8 same=1 forward-hash" | codex-perf-1 | 2026-03-28T19:39:39Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 8 total ops and 1 ops on one engine, with mixed-engine bundles. Kept the original hash stage order.
Code patch:
(none)
