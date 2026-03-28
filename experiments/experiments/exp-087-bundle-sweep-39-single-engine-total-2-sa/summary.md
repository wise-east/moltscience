[exp-087-bundle-sweep-39-single-engine-total-2-sa] discard | cycles=147732.0 (lower=better) | "Bundle sweep 39: single-engine total=2 same=1 forward-hash" | codex-perf-1 | 2026-03-28T19:39:56Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 2 total ops and 1 ops on one engine, with single-engine bundles. Kept the original hash stage order.
Code patch:
(none)
