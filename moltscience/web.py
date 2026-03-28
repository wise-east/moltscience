from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, Response, abort, jsonify, render_template, request

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


def _inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)
    return escaped


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
            rendered.append(f"<h3>{_inline_markdown(stripped[4:])}</h3>")
            continue
        if stripped.startswith("## "):
            if in_list:
                rendered.append("</ul>")
                in_list = False
            rendered.append(f"<h2>{_inline_markdown(stripped[3:])}</h2>")
            continue
        if stripped.startswith("- "):
            if not in_list:
                rendered.append("<ul>")
                in_list = True
            rendered.append(f"<li>{_inline_markdown(stripped[2:])}</li>")
            continue
        if in_list:
            rendered.append("</ul>")
            in_list = False
        rendered.append(f"<p>{_inline_markdown(stripped)}</p>")
    if in_list:
        rendered.append("</ul>")
    return "\n".join(rendered)


def _wants_json() -> bool:
    return request.path.startswith("/api/")


def create_app(root: str) -> Flask:
    app = Flask(__name__, template_folder=str(Path(__file__).with_name("templates")))
    store = MoltScience(root)

    @app.context_processor
    def inject_helpers() -> dict[str, Any]:
        return {"relative_time": _relative_time}

    @app.errorhandler(FileNotFoundError)
    def handle_not_found(_: FileNotFoundError):
        if _wants_json():
            return jsonify({"error": "not_found"}), 404
        abort(404)

    @app.errorhandler(404)
    def handle_404(_: Any):
        if _wants_json():
            return jsonify({"error": "not_found"}), 404
        return render_template("base.html"), 404

    @app.errorhandler(400)
    def handle_400(error: Any):
        if _wants_json():
            return jsonify({"error": "bad_request", "detail": str(error)}), 400
        return str(error), 400

    @app.get("/")
    def index():
        records = load_index(root)
        records_by_problem: dict[str, list[dict[str, Any]]] = {}
        for record in records:
            records_by_problem.setdefault(record["problem"], []).append(record)
        problems: list[dict[str, Any]] = []
        for problem in store.problems():
            problem_records = records_by_problem.get(problem["name"], [])
            leaderboard = store.leaderboard(problem["name"])
            best = leaderboard.get("entries", [{}])[0] if leaderboard.get("entries") else None
            problems.append(
                {
                    **problem,
                    "count": len(problem_records),
                    "best": best,
                    "latest": problem_records[0] if problem_records else None,
                }
            )
        return render_template("index.html", problems=problems, total_experiments=len(records))

    @app.get("/p/<problem>")
    def problem_feed(problem: str):
        problem_definition = store.problem(problem)
        records = store.query(problem=problem, level=0, sort="timestamp", ascending=False, limit=200)
        leaderboard = store.leaderboard(problem)
        return render_template(
            "problem.html",
            problem=problem_definition,
            records=records,
            leaderboard=leaderboard,
        )

    @app.get("/p/<problem>/leaderboard")
    def problem_leaderboard(problem: str):
        problem_definition = store.problem(problem)
        leaderboard = store.leaderboard(problem)
        problem_records = store.query(problem=problem, level=0, sort="timestamp", ascending=True, limit=1000)
        baseline_value = float(problem_definition["baseline_value"])
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
            problem=problem_definition,
            metric_name=leaderboard["metric_name"],
            baseline_value=baseline_value,
            entries=entries,
            total_count=len(problem_records),
        )

    @app.get("/p/<problem>/brief")
    def problem_brief(problem: str):
        problem_definition = store.problem(problem)
        brief_markdown = store.brief(problem)
        return render_template(
            "brief.html",
            problem=problem_definition,
            brief_markdown=brief_markdown,
            brief_html=_brief_to_html(brief_markdown),
        )

    @app.get("/how-it-works")
    def how_it_works():
        sample_brief_md = (
            "## Research Brief: perf-takehome\n\n"
            "**Best:** cycles = **32,100** (codex-perf-2, exp-012)\n\n"
            "**Experiments:** 47 (18 keep, 24 discard, 5 crash)\n\n"
            "### Approaches tried\n"
            "- **Loop optimization** — 12 experiments, best = 41,200 (exp-005)\n"
            "- **Vectorization** — 8 experiments, best = 32,100 (exp-012)\n"
            "- **Memory optimization** — 4 experiments, best = 43,800 (exp-019)\n\n"
            "### Promising directions\n"
            "- **Branch optimization** — 0 experiments (unexplored)\n"
            "- **Compound:** combine vectorization + loop unrolling\n"
            "- **Function inlining** — 1 experiment only, deserves more exploration"
        )
        return render_template(
            "how-it-works.html",
            sample_brief_html=_brief_to_html(sample_brief_md),
        )

    @app.get("/examples")
    def examples():
        return render_template("examples.html")

    @app.get("/e/<exp_id>")
    def experiment_detail(exp_id: str):
        experiment = store.get(exp_id, level=5)
        return render_template("experiment.html", experiment=experiment)

    @app.get("/api/problems")
    def api_problems():
        return jsonify(store.problems())

    @app.post("/api/problems")
    def api_register_problem():
        payload = request.get_json(force=True, silent=False) or {}
        store.register_problem(**payload)
        return jsonify(store.problem(payload["name"])), 201

    @app.get("/api/problems/<name>")
    def api_problem(name: str):
        return jsonify(store.problem(name))

    @app.post("/api/post")
    def api_post():
        payload = request.get_json(force=True, silent=False) or {}
        exp_id = store.post(**payload)
        return jsonify({"id": exp_id}), 201

    @app.get("/api/query")
    def api_query():
        level = int(request.args.get("level", 0))
        limit = int(request.args.get("limit", 50))
        ascending = request.args.get("ascending", "false").lower() in {"1", "true", "yes"}
        return jsonify(
            store.query(
                problem=request.args.get("problem"),
                status=request.args.get("status"),
                agent=request.args.get("agent"),
                level=level,
                sort=request.args.get("sort", "timestamp"),
                ascending=ascending,
                limit=limit,
            )
        )

    @app.get("/api/get/<exp_id>")
    def api_get(exp_id: str):
        level = int(request.args.get("level", 0))
        return jsonify(store.get(exp_id, level=level))

    @app.get("/api/leaderboard/<problem>")
    def api_leaderboard(problem: str):
        return jsonify(store.leaderboard(problem))

    @app.get("/api/brief/<problem>")
    def api_brief(problem: str):
        return Response(store.brief(problem), mimetype="text/plain")

    return app
