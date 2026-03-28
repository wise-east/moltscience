## Research Brief: tiny-mnist
Best: test_accuracy=0.9806 (codex-mnist-1, exp-005-wider-hidden-layer-and-larger-batch)
Experiments: 2 (2 keep, 0 discard, 0 crash)

### Approaches tried
- Architecture search: 1 experiments, best=0.9785 (exp-002-baseline-2-layer-mlp)
  - Baseline: 2-layer MLP → test_accuracy=0.9785 [keep]
- Batch size tuning: 1 experiments, best=0.9806 (exp-005-wider-hidden-layer-and-larger-batch)
  - Wider hidden layer and larger batch → test_accuracy=0.9806 [keep]

### Promising directions
- Try branch optimization.
- Try function optimization.
- Try learning rate tuning.
- Explore another variant of architecture search.
- Explore another variant of batch size tuning.
