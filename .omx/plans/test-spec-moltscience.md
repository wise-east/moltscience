# Test Spec: MoltScience 20-minute PRD run

## Goal

Define the minimum verification required to satisfy the Ralph planning gate and the Phase 1 BUILD checkpoint for MoltScience.

## Scope

- `moltscience/` package
- `tests/test_moltscience.py`
- Phase 1 CLI/API behavior
- Phase 2 posting of baseline experiments
- Phase 3/4 smoke verification artifacts

## Phase 1 acceptance tests

1. `post()` creates `manifest.json`, `summary.md`, and root indexes.
2. `query()` returns experiments and supports `problem` filtering.
3. `get(level=0)` exposes L0 fields; `get(level=2)` includes `motivation`.
4. `leaderboard()` sorts best-first by metric direction.
5. `brief()` returns non-empty markdown mentioning the problem.
6. `python -m moltscience post` followed by `python -m moltscience query` works in a subprocess round-trip.

Command:

```bash
python -m pytest tests/test_moltscience.py -v
```

## Phase 2 acceptance tests

1. At least one baseline is posted to `experiments/`.
2. Prefer both `perf-takehome` and `tiny-mnist`; if either setup fails, continue with the working problem and document the fallback.
3. `python -m moltscience brief --root experiments --problem <problem>` returns a non-empty brief.

## Phase 3 acceptance tests

1. Parallel research is launched via `omx team` if available.
2. If team launch fails, serial fallback posts additional experiments to MoltScience.
3. `experiments/index.json` and `experiments/leaderboard.json` update after research posts.

## Phase 4 acceptance tests

1. `demo/` contains generated artifacts summarizing the run.
2. Final verification re-runs Phase 1 tests and spot-checks experiment store contents.
