[exp-004-collapse-vector-child-index-parity-into-] keep | cycles=13376.0 (lower=better) | "Collapse vector child-index parity into multiply-add plus bit test" | codex-perf-2 | 2026-03-28T22:53:18Z
Methodology: Replaced the hot SIMD child-index update from modulo/equality/select logic with the equivalent arithmetic form 2*idx + 1 + (val & 1). In the vector loop this uses one multiply_add bundle plus one add bundle before the existing bounds-wrap step, cutting two bundles from every 8-lane chunk.
Code patch:
(none)
