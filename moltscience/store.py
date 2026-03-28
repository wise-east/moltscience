from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .brief import generate_brief
from .query import filter_and_sort_records, load_index, rebuild_index
from .render import render_experiment
from .schema import (
    DEFAULT_OPTIONAL_ARTIFACTS,
    DEFAULT_REQUIRED_ARTIFACTS,
    ExperimentStatus,
    Manifest,
    MetricDirection,
    ProblemDefinition,
)


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:40] or "experiment"


def _read_text(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def _read_json(path: Path, default: Any) -> Any:
    return json.loads(path.read_text()) if path.exists() else default


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n")


class MoltScience:
    def __init__(self, root: str) -> None:
        self.root = Path(root)
        self.experiments_dir = self.root / "experiments"
        self.problems_path = self.root / "problems.json"
        self.index_path = self.root / "index.json"
        self.leaderboard_path = self.root / "leaderboard.json"

        self.root.mkdir(parents=True, exist_ok=True)
        self.experiments_dir.mkdir(parents=True, exist_ok=True)
        for path, default in (
            (self.problems_path, []),
            (self.index_path, []),
            (self.leaderboard_path, {}),
        ):
            if not path.exists():
                _write_json(path, default)

    def _next_experiment_id(self, title: str) -> str:
        max_n = 0
        for path in self.experiments_dir.glob("exp-*-*"):
            match = re.match(r"exp-(\d+)-", path.name)
            if match:
                max_n = max(max_n, int(match.group(1)))
        return f"exp-{max_n + 1:03d}-{_slugify(title)}"

    def problems(self) -> list[dict[str, Any]]:
        return _read_json(self.problems_path, [])

    def problem(self, name: str) -> dict[str, Any]:
        for problem in self.problems():
            if problem["name"] == name:
                return problem
        raise FileNotFoundError(name)

    def register_problem(
        self,
        *,
        name: str,
        title: str,
        description: str,
        rules: str,
        metric_name: str,
        metric_direction: str,
        baseline_value: float,
        required_artifacts: list[str] | None = None,
        optional_artifacts: list[str] | None = None,
        categories: list[str] | None = None,
    ) -> None:
        definition = ProblemDefinition(
            name=name,
            title=title,
            description=description,
            rules=rules,
            metric_name=metric_name,
            metric_direction=MetricDirection(metric_direction),
            baseline_value=float(baseline_value),
            required_artifacts=list(required_artifacts or DEFAULT_REQUIRED_ARTIFACTS),
            optional_artifacts=list(optional_artifacts or DEFAULT_OPTIONAL_ARTIFACTS),
            categories=list(categories or []),
        )
        problems = self.problems()
        replaced = False
        for index, problem in enumerate(problems):
            if problem["name"] == name:
                problems[index] = definition.to_dict()
                replaced = True
                break
        if not replaced:
            problems.append(definition.to_dict())
        problems.sort(key=lambda item: item["name"])
        _write_json(self.problems_path, problems)

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
        parent_id: str | None = None,
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
            parent_id=parent_id,
            methodology=methodology,
            motivation=motivation,
            hypotheses=list(hypotheses or []),
            related_experiments=list(related_experiments or []),
            sub_experiments=list(sub_experiments or []),
        )
        _write_json(exp_dir / "manifest.json", manifest.to_dict())

        if code_patch:
            (exp_dir / "code.patch").write_text(code_patch)
        if motivation:
            (exp_dir / "motivation.md").write_text(motivation)
        if results is not None:
            _write_json(exp_dir / "results.json", results)
        if execution_log:
            (logs_dir / "execution.log").write_text(execution_log)
        if resources is not None:
            _write_json(logs_dir / "resources.json", resources)

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
        leaderboard = _read_json(self.leaderboard_path, {})
        if problem in leaderboard:
            return leaderboard[problem]
        try:
            problem_definition = self.problem(problem)
        except FileNotFoundError:
            return {"metric_name": "", "metric_direction": "", "entries": []}
        return {
            "metric_name": problem_definition["metric_name"],
            "metric_direction": problem_definition["metric_direction"],
            "entries": [],
        }

    def brief(self, problem: str) -> str:
        return generate_brief(self.root, problem)

    def rebuild_index(self) -> None:
        rebuild_index(self.root)
