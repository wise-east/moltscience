[exp-086-bundle-sweep-35-single-engine-total-3-sa] discard | cycles=147732.0 (lower=better) | "Bundle sweep 35: single-engine total=3 same=1 forward-hash" | codex-perf-2 | 2026-03-28T19:39:52Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 3 total ops and 1 ops on one engine, with single-engine bundles. Kept the original hash stage order.
Code patch:
(none)
