from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schema import ExperimentStatus, Manifest, MetricDirection


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def _manifest_paths(root: Path) -> list[Path]:
    experiments_dir = root / "experiments"
    if not experiments_dir.exists():
        return []
    return sorted(experiments_dir.glob("*/manifest.json"))


def rebuild_index(root: str | Path) -> list[dict[str, Any]]:
    root_path = Path(root)
    records: list[dict[str, Any]] = []
    for manifest_path in _manifest_paths(root_path):
        manifest = Manifest.from_dict(json.loads(manifest_path.read_text()))
        records.append(manifest.to_index_record())
    records.sort(key=lambda record: record["timestamp"], reverse=True)
    (root_path / "index.json").write_text(json.dumps(records, indent=2) + "\n")
    leaderboard = rebuild_leaderboard(root_path, records)
    (root_path / "leaderboard.json").write_text(json.dumps(leaderboard, indent=2) + "\n")
    return records


def rebuild_leaderboard(
    root: str | Path,
    index_records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    root_path = Path(root)
    records = index_records if index_records is not None else _read_json(root_path / "index.json", [])
    grouped: dict[str, dict[str, Any]] = {}
    for record in records:
        if record["status"] != ExperimentStatus.KEEP.value:
            continue
        if float(record["metric_value"]) <= 0:
            continue
        payload = grouped.setdefault(
            record["problem"],
            {
                "metric_name": record["metric_name"],
                "metric_direction": record["metric_direction"],
                "entries": [],
            },
        )
        payload["entries"].append(
            {
                "id": record["id"],
                "metric_value": record["metric_value"],
                "agent": record["agent"],
                "title": record["title"],
                "timestamp": record["timestamp"],
                "parent_id": record.get("parent_id"),
            }
        )
    for payload in grouped.values():
        reverse = payload["metric_direction"] == MetricDirection.HIGHER_IS_BETTER.value
        payload["entries"].sort(key=lambda item: item["metric_value"], reverse=reverse)
    return grouped


def load_index(root: str | Path) -> list[dict[str, Any]]:
    return _read_json(Path(root) / "index.json", [])


def filter_and_sort_records(
    records: list[dict[str, Any]],
    *,
    problem: str | None = None,
    status: str | None = None,
    agent: str | None = None,
    sort: str = "timestamp",
    ascending: bool = False,
    limit: int = 50,
) -> list[dict[str, Any]]:
    filtered = [
        record
        for record in records
        if (problem is None or record["problem"] == problem)
        and (status is None or record["status"] == status)
        and (agent is None or record["agent"] == agent)
    ]

    if sort == "metric_value":
        filtered.sort(
            key=lambda record: (
                -float(record["metric_value"])
                if record["metric_direction"] == MetricDirection.HIGHER_IS_BETTER.value
                else float(record["metric_value"])
            ),
            reverse=ascending,
        )
    else:
        filtered.sort(key=lambda record: record.get(sort, ""), reverse=not ascending)

    return filtered[:limit]
