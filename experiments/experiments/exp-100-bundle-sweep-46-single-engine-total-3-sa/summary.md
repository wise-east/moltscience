[exp-100-bundle-sweep-46-single-engine-total-3-sa] discard | cycles=147732.0 (lower=better) | "Bundle sweep 46: single-engine total=3 same=3 forward-hash" | codex-perf-1 | 2026-03-28T19:40:20Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 3 total ops and 3 ops on one engine, with single-engine bundles. Kept the original hash stage order.
Code patch:
(none)
