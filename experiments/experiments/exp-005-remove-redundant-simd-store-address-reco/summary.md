[exp-005-remove-redundant-simd-store-address-reco] keep | cycles=12864.0 (lower=better) | "Remove redundant SIMD store address recomputation" | codex-perf-1 | 2026-03-28T22:53:40Z
Methodology: Removed the redundant ALU bundle that recomputed tmp_addr1/tmp_addr2 before each vector vstore. The vector path already computed those addresses for the matching vload and never overwrote them, so the stores can reuse the original pointers directly.
Code patch:
(none)
