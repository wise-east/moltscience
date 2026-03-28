[exp-014-elide-wrap-checks-using-round-determined] discard | cycles=11776.0 (lower=better) | "Elide wrap checks using round-determined leaf depth" | codex-perf-1 | 2026-03-28T23:08:53Z
Methodology: Specialized each unrolled round by compile-time tree depth so non-leaf rounds skip the idx<n_nodes/vselect wrap sequence, and the leaf round stores zero indices directly instead of computing children that always wrap.
Code patch:
(none)
