[exp-025-overlap-next-batch-simd-prefetch-with-ve] discard | cycles=10215.0 (lower=better) | "Overlap next-batch SIMD prefetch with vector hash" | codex-perf-2 | 2026-03-28T23:16:30Z
Methodology: Added a double-buffered SIMD input path so the next batch’s index/value addresses are computed and vloaded during the first hash bundles of the current batch, while keeping the existing deterministic root and depth-1 cache fast paths intact.
Code patch:
(none)
