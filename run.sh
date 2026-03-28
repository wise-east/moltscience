#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

export PATH="/home/justin/ralphton/bin:/home/justin/.local/bin:/home/justin/bin:/home/justin/.nvm/versions/node/v22.22.1/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
export MOLTSCIENCE_START="$(date +%s)"
DEADLINE_MIN=170
MAX_CRASHES=8
SESSION_TIMEOUT_MIN=25

crash_count=0

echo "[run.sh] MoltScience autonomous build started at $(date)"
echo "[run.sh] Deadline: ${DEADLINE_MIN} minutes from now"

while true; do
    elapsed=$(python3 -c "import time,os; print(int((time.time()-float(os.environ['MOLTSCIENCE_START']))/60))")

    if [ "$elapsed" -ge "$DEADLINE_MIN" ]; then
        echo "[run.sh] Deadline reached (${elapsed} min). Stopping."
        break
    fi

    if [ "$crash_count" -ge "$MAX_CRASHES" ]; then
        echo "[run.sh] Too many crashes ($crash_count). Stopping."
        break
    fi

    remaining=$((DEADLINE_MIN - elapsed))
    timeout_min=$SESSION_TIMEOUT_MIN
    if [ "$remaining" -lt "$timeout_min" ]; then
        timeout_min=$remaining
    fi
    timeout_sec=$((timeout_min * 60))

    echo "[run.sh] Launching ralph (elapsed=${elapsed}min, remaining=${remaining}min, session_timeout=${timeout_min}min, crashes=${crash_count})"

    git add -A && git commit -m "checkpoint: pre-ralph-session-${crash_count} at ${elapsed}min" 2>/dev/null || true

    timeout "${timeout_sec}" omx ralph --full-auto \
        "Execute the MoltScience PRD at .omx/plans/prd-moltscience.md. \
Read AGENTS.md first, then follow the PRD phases. \
Elapsed so far: ${elapsed} minutes. You have ${remaining} minutes remaining. \
Check time gates in the PRD and commit checkpoints on schedule. \
Use .venv/bin/python (not python) for all Python commands. \
If you hit a content filter error, skip the current step and move to the next phase." || true

    git add -A && git commit -m "checkpoint: post-ralph-session-${crash_count} at $(python3 -c "import time,os; print(int((time.time()-float(os.environ['MOLTSCIENCE_START']))/60))")min" 2>/dev/null || true

    crash_count=$((crash_count + 1))
    echo "[run.sh] Ralph exited (session #${crash_count}). Restarting in 3s..."
    sleep 3
done

echo "[run.sh] Generating final report as fallback..."
mkdir -p demo
if [ -d experiments ] && command -v python3 &>/dev/null; then
    ./.venv/bin/python -m moltscience leaderboard --root experiments --problem perf-takehome > demo/leaderboard-perf.md 2>/dev/null || true
    ./.venv/bin/python -m moltscience leaderboard --root experiments --problem tiny-mnist > demo/leaderboard-mnist.md 2>/dev/null || true
    ./.venv/bin/python -m moltscience brief --root experiments --problem perf-takehome > demo/brief-perf.md 2>/dev/null || true
    ./.venv/bin/python -m moltscience brief --root experiments --problem tiny-mnist > demo/brief-mnist.md 2>/dev/null || true
fi

git add -A && git commit -m "final: autonomous run complete" 2>/dev/null || true
echo "[run.sh] Done at $(date)"
