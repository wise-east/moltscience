## Research Brief: perf-takehome
Best: cycles=147732.0 (codex-perf-1, exp-003-strip-debug-and-pause-bundles)
Experiments: 3 (2 keep, 1 discard, 0 crash)

### Approaches tried
- Optimizer tuning: 1 experiments, best=147734.0 (exp-001-baseline-unoptimized)
  - Baseline: unoptimized → cycles=147734.0 [keep]
- Other: 2 experiments, best=147732.0 (exp-004-replace-multiply-by-two-with-add)
  - Replace multiply-by-two with add → cycles=147732.0 [discard]
  - Strip debug and pause bundles → cycles=147732.0 [keep]

### Promising directions
- Try architecture search.
- Try batch size tuning.
- Try branch optimization.
- Explore another variant of optimizer tuning.
