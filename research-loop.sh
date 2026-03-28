#!/usr/bin/env bash
set -euo pipefail

AGENT_NAME="${1:?Usage: research-loop.sh <agent-name> <problem> <working-dir> [max-experiments]}"
PROBLEM="${2:?}"
WORKDIR="${3:?}"
MAX_EXPERIMENTS="${4:-100}"
API="http://localhost:8000"
CODEX="/home/justin/ralphton/bin/codex"

cd "$WORKDIR"
export PATH="/home/justin/ralphton/bin:/home/justin/.local/bin:/home/justin/bin:/home/justin/.nvm/versions/node/v22.22.1/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

echo "[${AGENT_NAME}] Starting research loop for ${PROBLEM} in ${WORKDIR}"
echo "[${AGENT_NAME}] Target: ${MAX_EXPERIMENTS} experiments"

exp_count=0
while [ "$exp_count" -lt "$MAX_EXPERIMENTS" ]; do
    exp_count=$((exp_count + 1))
    echo ""
    echo "[${AGENT_NAME}] === Experiment ${exp_count}/${MAX_EXPERIMENTS} ==="

    brief=$(curl -s "${API}/api/brief/${PROBLEM}" 2>/dev/null || echo "Brief unavailable")
    echo "[${AGENT_NAME}] Brief fetched ($(echo "$brief" | wc -c) bytes)"

    recent=$(curl -s "${API}/api/query?problem=${PROBLEM}&status=keep&limit=5" 2>/dev/null || echo "[]")

    $CODEX exec --dangerously-bypass-approvals-and-sandbox \
        "You are research agent ${AGENT_NAME} working on ${PROBLEM}.

STEP 1 — RESEARCH BRIEF (already fetched):
${brief}

STEP 2 — RECENT KEEPS:
${recent}

STEP 3 — YOUR TASK:
Pick ONE optimization from the brief's 'Promising directions' that has NOT been tried. Make a single focused change to the solution file. Read the full codebase first if this is your first experiment.

For perf-takehome: modify perf_takehome.py. Read problem.py to understand the machine model (slot limits, VALU vectorization, pipeline). The simulator counts clock cycles.
For tiny-mnist: modify train.py. The 90-second training budget is fixed.

STEP 4 — RUN:
perf-takehome: .venv/bin/python tests/submission_tests.py
tiny-mnist: .venv/bin/python train.py

STEP 5 — POST TO MOLTSCIENCE:
curl -s -X POST ${API}/api/post -H 'Content-Type: application/json' -d '{\"problem\":\"${PROBLEM}\",\"title\":\"<short desc>\",\"agent\":\"${AGENT_NAME}\",\"status\":\"<keep|discard|crash>\",\"metric_name\":\"<cycles or test_accuracy>\",\"metric_value\":<number>,\"metric_direction\":\"<lower_is_better or higher_is_better>\",\"methodology\":\"<what you changed>\",\"motivation\":\"<reference brief or prior exp>\"}'

STEP 6 — REVERT IF DISCARD/CRASH:
git checkout -- perf_takehome.py (or train.py)

Do exactly ONE experiment, post it, revert if needed, then exit." || true

    echo "[${AGENT_NAME}] Codex exited for experiment ${exp_count}"
    sleep 2
done

echo "[${AGENT_NAME}] Research loop complete. ${exp_count} experiments attempted."
