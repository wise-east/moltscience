[exp-052-bundle-sweep-25-single-engine-total-8-sa] discard | cycles=147732.0 (lower=better) | "Bundle sweep 25: single-engine total=8 same=4 forward-hash" | codex-perf-2 | 2026-03-28T19:39:05Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 8 total ops and 4 ops on one engine, with single-engine bundles. Kept the original hash stage order.
Code patch:
(none)
