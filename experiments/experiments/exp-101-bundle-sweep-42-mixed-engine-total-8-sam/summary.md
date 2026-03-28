[exp-101-bundle-sweep-42-mixed-engine-total-8-sam] discard | cycles=147732.0 (lower=better) | "Bundle sweep 42: mixed-engine total=8 same=2 forward-hash" | codex-perf-2 | 2026-03-28T19:40:20Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 8 total ops and 2 ops on one engine, with mixed-engine bundles. Kept the original hash stage order.
Code patch:
(none)
