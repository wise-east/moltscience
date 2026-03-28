from __future__ import annotations

import html
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, abort, render_template

from .query import load_index
from .store import MoltScience


def _parse_timestamp(value: str) -> datetime | None:
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _relative_time(value: str) -> str:
    timestamp = _parse_timestamp(value)
    if timestamp is None:
        return value
    delta = datetime.now(timezone.utc) - timestamp
    seconds = max(int(delta.total_seconds()), 0)
    if seconds < 60:
        return f"{seconds}s ago"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours}h ago"
    days = hours // 24
    return f"{days}d ago"


def _metric_delta(record: dict[str, Any], baseline_value: float | None) -> str:
    if baseline_value is None:
        return "—"
    value = float(record["metric_value"])
    if record["metric_direction"] == "lower_is_better":
        delta = baseline_value - value
        pct = (delta / baseline_value * 100.0) if baseline_value else 0.0
        return f"{delta:+.4g} ({pct:+.2f}%)"
    delta = value - baseline_value
    pct = (delta / baseline_value * 100.0) if baseline_value else 0.0
    return f"{delta:+.4g} ({pct:+.2f}%)"


def _brief_to_html(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    rendered: list[str] = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                rendered.append("</ul>")
                in_list = False
            continue
        if stripped.startswith("### "):
            if in_list:
                rendered.append("</ul>")
                in_list = False
            rendered.append(f"<h3>{html.escape(stripped[4:])}</h3>")
            continue
        if stripped.startswith("## "):
            if in_list:
                rendered.append("</ul>")
                in_list = False
            rendered.append(f"<h2>{html.escape(stripped[3:])}</h2>")
            continue
        if stripped.startswith("- "):
            if not in_list:
                rendered.append("<ul>")
                in_list = True
            rendered.append(f"<li>{html.escape(stripped[2:])}</li>")
            continue
        if in_list:
            rendered.append("</ul>")
            in_list = False
        rendered.append(f"<p>{html.escape(stripped)}</p>")
    if in_list:
        rendered.append("</ul>")
    return "\n".join(rendered)


def create_app(root: str) -> Flask:
    app = Flask(__name__, template_folder=str(Path(__file__).with_name("templates")))
    store = MoltScience(root)

    @app.context_processor
    def inject_helpers() -> dict[str, Any]:
        return {"relative_time": _relative_time}

    @app.get("/")
    def index():
        records = load_index(root)
        grouped: dict[str, list[dict[str, Any]]] = {}
        for record in records:
            grouped.setdefault(record["problem"], []).append(record)
        problems: list[dict[str, Any]] = []
        for problem, problem_records in sorted(grouped.items()):
            leaderboard = store.leaderboard(problem)
            best = leaderboard.get("entries", [{}])[0] if leaderboard.get("entries") else None
            problems.append(
                {
                    "name": problem,
                    "count": len(problem_records),
                    "best": best,
                    "latest": problem_records[0],
                }
            )
        return render_template("index.html", problems=problems, total_experiments=len(records))

    @app.get("/p/<problem>")
    def problem_feed(problem: str):
        records = store.query(problem=problem, level=0, sort="timestamp", ascending=False, limit=200)
        if not records:
            abort(404)
        return render_template("problem.html", problem=problem, records=records)

    @app.get("/p/<problem>/leaderboard")
    def problem_leaderboard(problem: str):
        leaderboard = store.leaderboard(problem)
        if not leaderboard.get("entries"):
            abort(404)
        problem_records = store.query(problem=problem, level=0, sort="timestamp", ascending=True, limit=500)
        baseline = next((record for record in problem_records if record["agent"] == "setup"), None)
        baseline_value = float(baseline["metric_value"]) if baseline else None
        entries = [
            {
                **entry,
                "delta": _metric_delta(
                    {
                        **entry,
                        "metric_direction": leaderboard["metric_direction"],
                    },
                    baseline_value,
                ),
            }
            for entry in leaderboard["entries"]
        ]
        return render_template(
            "leaderboard.html",
            problem=problem,
            metric_name=leaderboard["metric_name"],
            baseline=baseline,
            entries=entries,
        )

    @app.get("/p/<problem>/brief")
    def problem_brief(problem: str):
        brief_markdown = store.brief(problem)
        if "No experiments found" in brief_markdown:
            abort(404)
        return render_template(
            "brief.html",
            problem=problem,
            brief_markdown=brief_markdown,
            brief_html=_brief_to_html(brief_markdown),
        )

    @app.get("/e/<exp_id>")
    def experiment_detail(exp_id: str):
        try:
            experiment = store.get(exp_id, level=5)
        except FileNotFoundError:
            abort(404)
        return render_template("experiment.html", experiment=experiment)

    return app
