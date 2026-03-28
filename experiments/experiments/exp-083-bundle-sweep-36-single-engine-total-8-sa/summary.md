[exp-083-bundle-sweep-36-single-engine-total-8-sa] discard | cycles=147732.0 (lower=better) | "Bundle sweep 36: single-engine total=8 same=2 forward-hash" | codex-perf-1 | 2026-03-28T19:39:48Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 8 total ops and 2 ops on one engine, with single-engine bundles. Kept the original hash stage order.
Code patch:
(none)
