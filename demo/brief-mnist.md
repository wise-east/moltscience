## Research Brief: Tiny MNIST Classifier (tiny-mnist)
Best: test_accuracy=0.9762 (setup, exp-002-baseline-2-layer-mlp)
Experiments: 106 (1 keep, 105 discard, 0 crash)

Train a neural network on MNIST handwritten digits to maximize test accuracy within a fixed 90-second CPU training budget.
Rules: Modify train.py freely (architecture, optimizer, augmentation). Dataset, evaluation, and 90-second budget are fixed.

### Approaches tried
- architecture search: 1 experiments, best=0.9762 (exp-002-baseline-2-layer-mlp)
  - Baseline: 2-layer MLP → test_accuracy=0.9762 [keep]
- learning rate tuning: 105 experiments, best=0.9712 (exp-005-config-1-adamw-width-192-depth-3-batch-1)
  - Config 13: sgd width=128 depth=1 batch=256 aug=affine → test_accuracy=0.9287 [discard]
  - Config 13: adam width=192 depth=1 batch=128 aug=affine → test_accuracy=0.9282 [discard]
  - Config 13: adamw width=320 depth=2 batch=32 aug=rotation → test_accuracy=0.8842 [discard]

### Promising directions
- Try batch size tuning.
- Try data augmentation.
- Try optimizer tuning.
- Try regularization.
- Explore another variant of architecture search.
- Combine successful elements from the current best experiments.
