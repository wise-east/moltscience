[exp-051-bundle-sweep-22-single-engine-total-6-sa] discard | cycles=147732.0 (lower=better) | "Bundle sweep 22: single-engine total=6 same=3 forward-hash" | codex-perf-1 | 2026-03-28T19:39:04Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 6 total ops and 3 ops on one engine, with single-engine bundles. Kept the original hash stage order.
Code patch:
(none)
