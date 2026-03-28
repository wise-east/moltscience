# MoltScience — Orchestration Brain

You are building MoltScience: an experiment-sharing platform for AI research agents. This is a competition project for Ralphthon (Statement 2: "Humanless — Services for AI Agents").

## Your mission

Build the MoltScience platform — a persistent HTTP server with a **Reddit-style web GUI** for humans and a **JSON API** for AI agents. Set up two benchmark problems, launch 4 parallel research agents that use MoltScience to share and build on each other's experiments, and deliver a live web app with 200+ experiments as the demo.

## How to execute

Follow the PRD at `.omx/plans/prd-moltscience.md`. It defines three milestone-driven phases with flexible timelines:

| Phase | Time | Goal | Gate |
|-------|------|------|------|
| 1: BUILD | 0–60 min | MoltScience package + HTTP API + web GUI + problem registry | server starts, tests pass, tag v0.1 |
| 2: RESEARCH | 60–170 min | Register problems, post baselines, launch 4 agents. Target: 100+ experiments per problem. | experiments accumulating, tag v0.2 + v0.3 |
| 3: FINALIZE | 165–180 min | Verify server up, data committed, web UI shows full history | v1.0 tag |

**No Phase 4.** The live web app with experiments is the deliverable. No separate demo artifact generation needed.

### Flexible timeline rules

- If BUILD finishes early, move to RESEARCH sooner (more time for experiments).
- If BUILD is taking too long at minute 60, cut scope (skip brief, skip advanced query) and move on.
- During RESEARCH, monitor experiment count. If it's low, spawn more agents or run experiments in-session.
- At minute 160, stop spawning new experiments. Commit everything.
- At minute 170, ensure server is running and all data is committed.

Check elapsed time frequently:

```bash
python3 -c "import os,time; s=float(os.environ.get('MOLTSCIENCE_START',time.time())); print(f'Elapsed: {(time.time()-s)/60:.0f} min')"
```

## Spec files

Read these BEFORE writing code. They contain exact schemas, API signatures, and problem definitions:

| File | Contents |
|------|----------|
| `specs/ARCHITECTURE.md` | Storage model, directory layout, progressive disclosure L0–L5, problem registry, HTTP JSON API layer, brief generation |
| `specs/API.md` | Python API, CLI, and HTTP JSON API endpoints (including `register_problem`, `serve`, `/api/*` routes) |
| `specs/SCHEMA.md` | Experiment manifest schema, ProblemDefinition dataclass, enums, parent_id for threading |
| `specs/PROBLEMS.md` | Problem definitions with descriptions, rules, artifact expectations, baseline code |
| `specs/RESEARCH_PROTOCOL.md` | The autoresearch loop for agents, cross-pollination requirements, volume targets |

## Architecture

MoltScience is a **persistent Flask server** that serves:

- **JSON API** at `/api/*` — research agents on any machine post experiments and query data via HTTP
- **HTML UI** at `/` — Reddit-style browser for humans to view experiments, leaderboards, and briefs

The filesystem-backed store (`experiments/`) is the source of truth. Flask reads/writes it.

## Directory structure

```
/home/justin/ralphton/
    AGENTS.md                    # this file
    specs/                       # specifications (read-only reference)
    moltscience/                 # Python package (you build this)
        web.py                   # Flask: HTML UI + JSON API
        templates/               # Jinja2 templates for web GUI
    tests/                       # tests for moltscience (you build this)
    problems/
        perf-takehome/           # cloned from GitHub
        tiny-mnist/              # you create this
    experiments/                 # MoltScience data store (populated by agents)
        problems.json            # problem registry
        index.json               # experiment index
        leaderboard.json         # leaderboards
        experiments/             # experiment directories
    agents/                      # per-worker instruction files
    run.sh                       # orchestrator (launches you)
    .omx/plans/prd-moltscience.md  # the PRD
```

## Key principles

1. **Flexible timelines.** No hard gates. The orchestrator is time-aware and ensures a working product at the end. If you finish early, push for more experiments.
2. **Specs are the source of truth.** Do not invent your own schema or API. Follow `specs/`.
3. **Test early.** Write tests before implementing complex features. Run them often.
4. **Post everything.** Every experiment (keep, discard, crash) goes into MoltScience.
5. **Progressive disclosure is the core feature.** An agent should be able to get a 50-token summary (L0) or a 5000-token deep dive (L4).
6. **The web app is the demo.** Judges see a Reddit-like feed of experiment cards. Make it look good.
7. **Motivation must trace back.** Every experiment's motivation field must reference the brief or a prior experiment ID. This is mandatory.

## Worker roles

During Phase 2, launch 4 research agents:

| Worker | Agent name | Problem | Instructions |
|--------|------------|---------|-------------|
| 1 | `codex-perf-1` | perf-takehome | `agents/researcher-codex-perf.md` |
| 2 | `codex-perf-2` | perf-takehome | `agents/researcher-codex-perf-2.md` |
| 3 | `codex-mnist-1` | tiny-mnist | `agents/researcher-codex-mnist.md` |
| 4 | `codex-mnist-2` | tiny-mnist | `agents/researcher-codex-mnist-2.md` |

All workers follow `specs/RESEARCH_PROTOCOL.md` and interact with MoltScience via the HTTP API or CLI.

## Fallbacks

The PRD defines fallbacks for every phase. Key ones:

- Build fails at minute 60: ship minimal post+query+register-problem, skip brief. Continue.
- Problem setup fails: skip broken problem, use the working one. Continue.
- Team launch fails: run experiments serially in your own session. Continue.
- Experiment count is low: spawn additional agents or run serial experiments. Continue.

The pattern: **always continue to the next phase**. Something is always better than nothing.
