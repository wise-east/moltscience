[exp-018-pipeline-next-batch-prefetch-under-vecto] keep | cycles=9392.0 (lower=better) | "Pipeline next-batch prefetch under vector hash" | codex-perf-1 | 2026-03-28T23:12:09Z
Methodology: Added a two-buffer vector software pipeline in perf_takehome.py so the next SIMD batch’s base-address setup, vloads, and gather-loads execute in parallel with the current batch’s hash bundles. I also folded the final store-address recomputation into the bounds-check bundle so ALU slots stay occupied while the VALU compare runs.
Code patch:
(none)
