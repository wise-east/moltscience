[exp-059-bundle-sweep-26-single-engine-total-6-sa] discard | cycles=147732.0 (lower=better) | "Bundle sweep 26: single-engine total=6 same=1 forward-hash" | codex-perf-1 | 2026-03-28T19:39:18Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 6 total ops and 1 ops on one engine, with single-engine bundles. Kept the original hash stage order.
Code patch:
(none)
