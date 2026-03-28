from __future__ import annotations

import argparse
import json
from pathlib import Path

from .render import render_experiment, render_leaderboard
from .store import MoltScience


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m moltscience")
    subparsers = parser.add_subparsers(dest="command", required=True)

    post = subparsers.add_parser("post")
    post.add_argument("--root", required=True)
    post.add_argument("--problem", required=True)
    post.add_argument("--title", required=True)
    post.add_argument("--agent", required=True)
    post.add_argument("--status", required=True)
    post.add_argument("--metric-name", required=True)
    post.add_argument("--metric-value", required=True, type=float)
    post.add_argument("--metric-direction", required=True)
    post.add_argument("--methodology", default="")
    post.add_argument("--motivation", default="")
    post.add_argument("--code-patch-file")
    post.add_argument("--execution-log-file")
    post.add_argument("--resources-json")

    query = subparsers.add_parser("query")
    query.add_argument("--root", required=True)
    query.add_argument("--problem")
    query.add_argument("--status")
    query.add_argument("--agent")
    query.add_argument("--level", type=int, default=0)
    query.add_argument("--sort", default="timestamp")
    query.add_argument("--ascending", action="store_true")
    query.add_argument("--limit", type=int, default=50)

    get = subparsers.add_parser("get")
    get.add_argument("--root", required=True)
    get.add_argument("--id", required=True)
    get.add_argument("--level", type=int, default=0)

    leaderboard = subparsers.add_parser("leaderboard")
    leaderboard.add_argument("--root", required=True)
    leaderboard.add_argument("--problem", required=True)

    brief = subparsers.add_parser("brief")
    brief.add_argument("--root", required=True)
    brief.add_argument("--problem", required=True)

    serve = subparsers.add_parser("serve")
    serve.add_argument("--root", required=True)
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--host", default="0.0.0.0")
    return parser


def _read_optional_file(path: str | None) -> str:
    return Path(path).read_text() if path else ""


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "serve":
        from .web import create_app

        app = create_app(args.root)
        app.run(host=args.host, port=args.port)
        return 0

    store = MoltScience(args.root)

    if args.command == "post":
        exp_id = store.post(
            problem=args.problem,
            title=args.title,
            agent=args.agent,
            status=args.status,
            metric_name=args.metric_name,
            metric_value=args.metric_value,
            metric_direction=args.metric_direction,
            methodology=args.methodology,
            motivation=args.motivation,
            code_patch=_read_optional_file(args.code_patch_file),
            execution_log=_read_optional_file(args.execution_log_file),
            resources=json.loads(args.resources_json) if args.resources_json else None,
        )
        print(exp_id)
        return 0

    if args.command == "query":
        experiments = store.query(
            problem=args.problem,
            status=args.status,
            agent=args.agent,
            level=args.level,
            sort=args.sort,
            ascending=args.ascending,
            limit=args.limit,
        )
        for index, experiment in enumerate(experiments):
            if index:
                print()
            print(render_experiment(experiment, level=args.level))
        return 0

    if args.command == "get":
        print(render_experiment(store.get(args.id, level=args.level), level=args.level))
        return 0

    if args.command == "leaderboard":
        print(render_leaderboard(args.problem, store.leaderboard(args.problem)))
        return 0

    if args.command == "brief":
        print(store.brief(args.problem))
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2
