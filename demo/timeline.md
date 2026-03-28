# Experiment Timeline

- **2026-03-28T18:39:47Z** — `setup` ran **Baseline: unoptimized** on `perf-takehome` → cycles=147734.0 [keep]  
  Methodology: Original unoptimized code from the Anthropic performance takehome repository.

- **2026-03-28T18:40:59Z** — `setup` ran **Baseline: 2-layer MLP** on `tiny-mnist` → test_accuracy=0.9785 [keep]  
  Methodology: Baseline 2-layer MLP from the PRD trained for the fixed 90-second CPU budget.

- **2026-03-28T18:44:12Z** — `codex-perf-1` ran **Strip debug and pause bundles** on `perf-takehome` → cycles=147732.0 [keep]  
  Methodology: Removed generated debug compare instructions and pause bundles from the emitted kernel because the frozen submission harness disables both features while still paying for instruction bundles.

- **2026-03-28T18:44:31Z** — `claude-perf-1` ran **Replace multiply-by-two with add** on `perf-takehome` → cycles=147732.0 [discard]  
  Methodology: Replaced the multiply-by-two step in next-index computation with a self-add to test whether the ALU handles doubling cheaper than general multiplication.

- **2026-03-28T18:45:24Z** — `codex-mnist-1` ran **Wider hidden layer and larger batch** on `tiny-mnist` → test_accuracy=0.9806 [keep]  
  Methodology: Increased the hidden width from 128 to 256 and doubled batch size to 128 to trade slightly larger capacity for faster batch throughput within the same 90-second wall-clock budget.

