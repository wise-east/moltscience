<ralph_native_subagents>
You are in OMX Ralph persistence mode.
Primary task: Execute the MoltScience PRD at .omx/plans/prd-moltscience.md. Read AGENTS.md first, then follow the PRD phases. This is a 20-minute test run. You have 19 minutes. Work fast. Use .venv/bin/python for all Python commands. The moltscience package is already built - verify tests pass then move to Phase 2. If you hit content filter errors, skip and move to the next phase.
Parallelism guidance:
- Prefer Codex native subagents for independent parallel subtasks.
- Treat `.omx/state/subagent-tracking.json` as the native subagent activity ledger for this session.
- Do not declare the task complete, and do not transition into final verification/completion, while active native subagent threads are still running.
- Before closing a verification wave, confirm that active native subagent threads have drained.
Final deslop guidance:
- Step 7.5 must run oh-my-codex:ai-slop-cleaner in standard mode on changed files only, using the repo-relative paths listed in `.omx/ralph/changed-files.txt`.
- Keep the cleaner scope bounded to that file list; do not widen the pass to the full codebase or unrelated files.
- Step 7.6 must rerun the current tests/build/lint verification after ai-slop-cleaner; if regression fails, roll back cleaner changes or fix and retry before completion.
</ralph_native_subagents>
