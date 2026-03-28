## Research Brief: Anthropic Performance Takehome (perf-takehome)
Best: cycles=147732.0 (setup, exp-001-baseline-unoptimized)
Experiments: 101 (1 keep, 52 discard, 48 crash)

Optimize code running on a simulated processor to minimize clock cycles. A custom VM executes your solution and counts cycles.
Rules: Modify only perf_takehome.py. The simulator (problem.py) and tests/ are read-only.

### Approaches tried
- other: 101 experiments, best=147732.0 (exp-111-bundle-sweep-49-single-engine-total-4-sa)
  - Bundle sweep 49: single-engine total=4 same=1 forward-hash → cycles=147732.0 [discard]
  - Bundle sweep 48: single-engine total=6 same=2 forward-hash → cycles=147732.0 [discard]
  - Bundle sweep 47: single-engine total=8 same=2 forward-hash → cycles=147732.0 [discard]

### Promising directions
- Try algorithmic improvement.
- Try branch optimization.
- Try function optimization.
- Try loop optimization.
- Combine successful elements from the current best experiments.
