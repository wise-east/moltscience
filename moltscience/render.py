from __future__ import annotations

from typing import Any


def render_experiment(experiment: dict[str, Any], level: int = 0) -> str:
    metric = (
        f'{experiment["metric_name"]}={experiment["metric_value"]} '
        f'({"lower" if experiment["metric_direction"] == "lower_is_better" else "higher"}=better)'
    )
    lines = [
        f'[{experiment["id"]}] {experiment["status"]} | {metric} | '
        f'"{experiment["title"]}" | {experiment["agent"]} | {experiment["timestamp"]}'
    ]
    if level >= 1:
        lines.extend(
            [
                f"Methodology: {experiment.get('methodology', '') or '(none)'}",
                "Code patch:",
                experiment.get("code_patch", "") or "(none)",
            ]
        )
    if level >= 2:
        lines.extend(
            [
                f"Motivation: {experiment.get('motivation', '') or '(none)'}",
                f"Hypotheses: {experiment.get('hypotheses', [])}",
                f"Related experiments: {experiment.get('related_experiments', [])}",
                f"Sub-experiments: {experiment.get('sub_experiments', [])}",
            ]
        )
    if level >= 3:
        lines.append(f"Results: {experiment.get('results', {})}")
    if level >= 4:
        lines.append(f"Execution log:\n{experiment.get('execution_log', '') or '(none)'}")
    if level >= 5:
        lines.append(f"Resources: {experiment.get('resources', {})}")
    return "\n".join(lines)


def render_leaderboard(problem: str, leaderboard: dict[str, Any]) -> str:
    if not leaderboard.get("entries"):
        return f"## Leaderboard: {problem}\n\nNo keep experiments found."
    lines = [
        f"## Leaderboard: {problem}",
        "",
        "| Rank | ID | Metric | Agent | Title | Timestamp |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for rank, entry in enumerate(leaderboard["entries"], start=1):
        lines.append(
            f"| {rank} | {entry['id']} | {entry['metric_value']} | {entry['agent']} | "
            f"{entry['title']} | {entry['timestamp']} |"
        )
    return "\n".join(lines)
