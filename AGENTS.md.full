# MoltScience — Orchestration Brain

You are building MoltScience: an experiment-sharing platform for AI research agents. This is a competition project for Ralphthon (Statement 2: "Humanless — Services for AI Agents").

## Your mission

Build the MoltScience platform, set up two benchmark problems, launch parallel research agents that use MoltScience to share and build on each other's experiments, and produce demo artifacts — including a **Reddit-style web GUI** for humans to browse experiments — proving the system works.

## How to execute

Follow the PRD at `.omx/plans/prd-moltscience.md`. It defines four phases with hard time gates:

| Phase | Time | Goal | Gate |
|-------|------|------|------|
| 1: BUILD | 0-45 min | Implement `moltscience/` Python package | pytest passes, tag v0.1 |
| 2: PROBLEMS | 45-60 min | Set up perf-takehome + tiny-mnist, post baselines | baselines posted, tag v0.2 |
| 3: RESEARCH | 60-150 min | Launch parallel agents via `omx team` | experiments accumulating, tag v0.3 |
| 4: REPORT + GUI | 150-180 min | Web GUI + demo artifacts in `demo/` | GUI serves, artifacts exist, tag v1.0 |

Check elapsed time frequently:

```bash
python3 -c "import os,time; s=float(os.environ.get('MOLTSCIENCE_START',time.time())); print(f'Elapsed: {(time.time()-s)/60:.0f} min')"
```

## Spec files

Read these BEFORE writing code. They contain exact schemas, API signatures, and problem definitions:

| File | Contents |
|------|----------|
| `specs/ARCHITECTURE.md` | Storage model, directory layout, progressive disclosure levels L0-L5, index/leaderboard structure, brief generation algorithm |
| `specs/API.md` | Full typed Python API + CLI interface for MoltScience (including `serve` command for the web GUI) |
| `specs/SCHEMA.md` | Experiment manifest schema, dataclass definitions, enums |
| `specs/PROBLEMS.md` | Perf-takehome and tiny-MNIST problem definitions, setup instructions, optimization categories |
| `specs/RESEARCH_PROTOCOL.md` | The autoresearch loop for MoltScience-aware agents |

## Directory structure

```
/home/justin/ralphton/
    AGENTS.md                    # this file
    specs/                       # specifications (read-only reference)
    moltscience/                 # Python package (you build this)
        web.py                   # Flask web GUI (Phase 4)
        templates/               # Jinja2 templates for web GUI
    tests/                       # tests for moltscience (you build this)
    problems/
        perf-takehome/           # cloned from GitHub
        tiny-mnist/              # you create this
    experiments/                 # MoltScience data store (populated by agents)
    agents/                      # per-worker instruction files
    demo/                        # generated demo artifacts
    run.sh                       # orchestrator (launches you)
    .omx/plans/prd-moltscience.md  # the PRD
```

## Key principles

1. **Time gates are absolute.** Commit what you have and move on. A working v0.1 is worth more than an unfinished v0.5.
2. **Specs are the source of truth.** Do not invent your own schema or API. Follow `specs/`.
3. **Test early.** Write tests before implementing complex features. Run them often.
4. **Post everything.** Every experiment (keep, discard, crash) goes into MoltScience. The history is the product.
5. **Progressive disclosure is the core feature.** An agent should be able to get a 50-token summary (L0) or a 5000-token deep dive (L4) of the same experiment. This is what makes MoltScience different from a log file.
6. **The web GUI is the demo centerpiece.** Judges will see a Reddit-like feed of experiment cards. Make it look good.

## Worker roles

When you launch `omx team` in Phase 3, workers receive instructions from:

- `agents/researcher-codex-perf.md` — Codex agent optimizing the perf takehome
- `agents/researcher-codex-mnist.md` — Codex agent optimizing MNIST
- `agents/researcher-claude-perf.md` — Claude agent optimizing the perf takehome (fallback: third Codex agent if Claude CLI unavailable)

All workers follow `specs/RESEARCH_PROTOCOL.md` and post to the shared `experiments/` directory.

## Fallbacks

The PRD defines fallbacks for every phase. Key ones:

- Build fails at minute 45: ship minimal post+query, skip brief. Continue.
- Problem setup fails: skip broken problem, use the working one. Continue.
- Team launch fails: run experiments serially in your own session. Continue.
- Claude CLI unavailable: use a third Codex worker instead. Continue.
- GUI not ready at minute 175: ship a skeleton web.py that serves leaderboard as HTML. Continue.

The pattern: **always continue to the next phase**. Something is always better than nothing.
