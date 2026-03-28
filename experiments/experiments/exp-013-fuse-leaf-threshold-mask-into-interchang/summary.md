[exp-013-fuse-leaf-threshold-mask-into-interchang] keep | cycles=10913.0 (lower=better) | "Fuse leaf-threshold mask into interchanged SIMD rounds" | codex-perf-2 | 2026-03-28T23:08:40Z
Methodology: Combined the earlier leaf-threshold wraparound idea with the current batch-major SIMD kernel. I broadcast the internal-node cutoff once, compute a per-lane descend mask alongside the forest address at the start of each round, and reuse that mask for the final vselect so the vector path no longer needs a separate post-update idx<n_nodes bundle.
Code patch:
(none)
