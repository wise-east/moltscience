[exp-039-bundle-sweep-17-single-engine-total-4-sa] discard | cycles=147732.0 (lower=better) | "Bundle sweep 17: single-engine total=4 same=4 forward-hash" | codex-perf-1 | 2026-03-28T19:38:45Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 4 total ops and 4 ops on one engine, with single-engine bundles. Kept the original hash stage order.
Code patch:
(none)
