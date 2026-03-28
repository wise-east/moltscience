[exp-015-bundle-sweep-4-single-engine-total-4-sam] discard | cycles=147732.0 (lower=better) | "Bundle sweep 4: single-engine total=4 same=2 forward-hash" | codex-perf-1 | 2026-03-28T19:37:58Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 4 total ops and 2 ops on one engine, with single-engine bundles. Kept the original hash stage order.
Code patch:
(none)
