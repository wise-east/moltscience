from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .brief import generate_brief
from .query import filter_and_sort_records, load_index, rebuild_index
from .render import render_experiment
from .schema import ExperimentStatus, Manifest, MetricDirection


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:40] or "experiment"


def _read_text(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def _read_json(path: Path, default: Any) -> Any:
    return json.loads(path.read_text()) if path.exists() else default


class MoltScience:
    def __init__(self, root: str) -> None:
        self.root = Path(root)
        self.experiments_dir = self.root / "experiments"
        self.root.mkdir(parents=True, exist_ok=True)
        self.experiments_dir.mkdir(parents=True, exist_ok=True)
        for path, default in (
            (self.root / "index.json", []),
            (self.root / "leaderboard.json", {}),
        ):
            if not path.exists():
                path.write_text(json.dumps(default, indent=2) + "\n")

    def _next_experiment_id(self, title: str) -> str:
        max_n = 0
        for path in self.experiments_dir.glob("exp-*-*"):
            match = re.match(r"exp-(\d+)-", path.name)
            if match:
                max_n = max(max_n, int(match.group(1)))
        return f"exp-{max_n + 1:03d}-{_slugify(title)}"

    def post(
        self,
        *,
        problem: str,
        title: str,
        agent: str,
        status: str,
        metric_name: str,
        metric_value: float,
        metric_direction: str,
        methodology: str = "",
        code_patch: str = "",
        motivation: str = "",
        hypotheses: list[str] | None = None,
        related_experiments: list[str] | None = None,
        sub_experiments: list[dict] | None = None,
        results: dict | None = None,
        execution_log: str = "",
        resources: dict | None = None,
    ) -> str:
        try:
            parsed_status = ExperimentStatus(status)
        except ValueError as exc:
            raise ValueError(f"Unknown status: {status}") from exc
        try:
            parsed_direction = MetricDirection(metric_direction)
        except ValueError as exc:
            raise ValueError(f"Unknown metric_direction: {metric_direction}") from exc

        exp_id = self._next_experiment_id(title)
        exp_dir = self.experiments_dir / exp_id
        logs_dir = exp_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

        manifest = Manifest(
            id=exp_id,
            problem=problem,
            title=title,
            agent=agent,
            status=parsed_status,
            metric_name=metric_name,
            metric_value=float(metric_value),
            metric_direction=parsed_direction,
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            methodology=methodology,
            motivation=motivation,
            hypotheses=list(hypotheses or []),
            related_experiments=list(related_experiments or []),
            sub_experiments=list(sub_experiments or []),
        )
        (exp_dir / "manifest.json").write_text(json.dumps(manifest.to_dict(), indent=2) + "\n")

        if code_patch:
            (exp_dir / "code.patch").write_text(code_patch)
        if motivation:
            (exp_dir / "motivation.md").write_text(motivation)
        if results is not None:
            (exp_dir / "results.json").write_text(json.dumps(results, indent=2) + "\n")
        if execution_log:
            (logs_dir / "execution.log").write_text(execution_log)
        if resources is not None:
            (logs_dir / "resources.json").write_text(json.dumps(resources, indent=2) + "\n")

        summary = render_experiment(
            {
                **manifest.to_index_record(),
                "methodology": methodology,
                "code_patch": code_patch,
            },
            level=1,
        )
        (exp_dir / "summary.md").write_text(summary + "\n")

        rebuild_index(self.root)
        return exp_id

    def get(self, exp_id: str, level: int = 0) -> dict[str, Any]:
        exp_dir = self.experiments_dir / exp_id
        manifest_path = exp_dir / "manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(exp_id)

        manifest = Manifest.from_dict(json.loads(manifest_path.read_text()))
        record: dict[str, Any] = manifest.to_index_record()
        if level >= 1:
            record["methodology"] = manifest.methodology
            record["code_patch"] = _read_text(exp_dir / "code.patch")
        if level >= 2:
            record["motivation"] = _read_text(exp_dir / "motivation.md") or manifest.motivation
            record["hypotheses"] = manifest.hypotheses
            record["related_experiments"] = manifest.related_experiments
            record["sub_experiments"] = manifest.sub_experiments
        if level >= 3:
            record["results"] = _read_json(exp_dir / "results.json", {})
        if level >= 4:
            record["execution_log"] = _read_text(exp_dir / "logs" / "execution.log")
        if level >= 5:
            record["resources"] = _read_json(exp_dir / "logs" / "resources.json", {})
        return record

    def query(
        self,
        *,
        problem: str | None = None,
        status: str | None = None,
        agent: str | None = None,
        level: int = 0,
        sort: str = "timestamp",
        ascending: bool = False,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        records = filter_and_sort_records(
            load_index(self.root),
            problem=problem,
            status=status,
            agent=agent,
            sort=sort,
            ascending=ascending,
            limit=limit,
        )
        if level <= 0:
            return records
        return [self.get(record["id"], level=level) for record in records]

    def leaderboard(self, problem: str) -> dict[str, Any]:
        leaderboard = _read_json(self.root / "leaderboard.json", {})
        return leaderboard.get(problem, {"metric_name": "", "metric_direction": "", "entries": []})

    def brief(self, problem: str) -> str:
        return generate_brief(self.root, problem)

    def rebuild_index(self) -> None:
        rebuild_index(self.root)
