[exp-008-bundle-sweep-2-mixed-engine-total-2-same] discard | cycles=147732.0 (lower=better) | "Bundle sweep 2: mixed-engine total=2 same=2 forward-hash" | codex-perf-2 | 2026-03-28T19:37:46Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 2 total ops and 2 ops on one engine, with mixed-engine bundles. Kept the original hash stage order.
Code patch:
(none)
