[exp-007-bundle-sweep-1-single-engine-total-6-sam] discard | cycles=147732.0 (lower=better) | "Bundle sweep 1: single-engine total=6 same=4 forward-hash" | codex-perf-1 | 2026-03-28T19:37:45Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 6 total ops and 4 ops on one engine, with single-engine bundles. Kept the original hash stage order.
Code patch:
(none)
