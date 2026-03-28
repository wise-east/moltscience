[exp-111-bundle-sweep-49-single-engine-total-4-sa] discard | cycles=147732.0 (lower=better) | "Bundle sweep 49: single-engine total=4 same=1 forward-hash" | codex-perf-2 | 2026-03-28T19:40:48Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 4 total ops and 1 ops on one engine, with single-engine bundles. Kept the original hash stage order.
Code patch:
(none)
