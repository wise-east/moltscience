from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from .query import load_index
from .schema import ExperimentStatus, MetricDirection, ProblemDefinition


CATEGORY_KEYWORDS = [
    (("unroll", "loop"), "loop optimization"),
    (("simd", "vector", "avx"), "vectorization"),
    (("cache", "align", "prefetch", "memory"), "memory optimization"),
    (("branch", "predict", "cmov"), "branch optimization"),
    (("inline", "flatten", "function"), "function optimization"),
    (("algorithm", "rewrite"), "algorithmic improvement"),
    (("lr", "learning rate"), "learning rate tuning"),
    (("batch", "batch size"), "batch size tuning"),
    (("architecture", "layer", "hidden", "width", "depth"), "architecture search"),
    (("optimizer", "adam", "adamw", "sgd", "momentum"), "optimizer tuning"),
    (("dropout", "weight decay", "regularization"), "regularization"),
    (("augmentation", "augment", "rotation", "affine"), "data augmentation"),
]


def _load_problem(root: Path, problem: str) -> ProblemDefinition | None:
    problems_path = root / "problems.json"
    if not problems_path.exists():
        return None
    for item in json.loads(problems_path.read_text()):
        if item["name"] == problem:
            return ProblemDefinition.from_dict(item)
    return None


def _keyword_matches(haystack: str, keyword: str) -> bool:
    escaped = re.escape(keyword.lower())
    if " " in keyword or "-" in keyword:
        return re.search(rf"(?<!\w){escaped}(?!\w)", haystack) is not None
    return re.search(rf"\b{escaped}\b", haystack) is not None


def categorize(title: str, methodology: str, categories: list[str] | None = None) -> str:
    haystack = f"{title} {methodology}".lower()
    allowed_categories = set(categories or [])
    for keywords, category in CATEGORY_KEYWORDS:
        if allowed_categories and category not in allowed_categories:
            continue
        if any(_keyword_matches(haystack, keyword) for keyword in keywords):
            return category
    return "other"


def _best_record(records: list[dict[str, Any]]) -> dict[str, Any]:
    comparable_records = [
        record for record in records if record["status"] != ExperimentStatus.CRASH.value
    ] or records
    direction = comparable_records[0]["metric_direction"]
    return sorted(
        comparable_records,
        key=lambda record: record["metric_value"],
        reverse=direction == MetricDirection.HIGHER_IS_BETTER.value,
    )[0]


def generate_brief(root: str | Path, problem: str) -> str:
    root_path = Path(root)
    problem_definition = _load_problem(root_path, problem)
    experiments = [record for record in load_index(root_path) if record["problem"] == problem]

    heading = f"## Research Brief: {problem}"
    if problem_definition is not None:
        heading = f"## Research Brief: {problem_definition.title} ({problem})"

    if not experiments:
        lines = [heading, "", f"No experiments found for {problem}."]
        if problem_definition is not None and problem_definition.categories:
            lines.extend(["", "### Suggested starting directions"])
            lines.extend(f"- Try {category}." for category in problem_definition.categories[:4])
        return "\n".join(lines)

    keep = [record for record in experiments if record["status"] == ExperimentStatus.KEEP.value]
    discard = [record for record in experiments if record["status"] == ExperimentStatus.DISCARD.value]
    crash = [record for record in experiments if record["status"] == ExperimentStatus.CRASH.value]

    if keep:
        direction = keep[0]["metric_direction"]
        best = sorted(
            keep,
            key=lambda record: record["metric_value"],
            reverse=direction == MetricDirection.HIGHER_IS_BETTER.value,
        )[0]
        best_line = (
            f"Best: {best['metric_name']}={best['metric_value']} "
            f"({best['agent']}, {best['id']})"
        )
    else:
        best_line = "Best: no keep experiments yet"

    categories: dict[str, list[dict[str, Any]]] = defaultdict(list)
    tried_categories: set[str] = set()
    for record in experiments:
        methodology = ""
        manifest_path = root_path / "experiments" / record["id"] / "manifest.json"
        if manifest_path.exists():
            methodology = json.loads(manifest_path.read_text()).get("methodology", "")
        category = categorize(
            record["title"],
            methodology,
            problem_definition.categories if problem_definition is not None else None,
        )
        categories[category].append(record)
        tried_categories.add(category)

    lines = [
        heading,
        best_line,
        f"Experiments: {len(experiments)} ({len(keep)} keep, {len(discard)} discard, {len(crash)} crash)",
    ]
    if problem_definition is not None:
        lines.extend(["", problem_definition.description, f"Rules: {problem_definition.rules}"])
    lines.extend(["", "### Approaches tried"])
    for category, records in sorted(categories.items()):
        best_record = _best_record(records)
        lines.append(
            f"- {category}: {len(records)} experiments, best={best_record['metric_value']} ({best_record['id']})"
        )
        for record in records[:3]:
            lines.append(
                f"  - {record['title']} → {record['metric_name']}={record['metric_value']} [{record['status']}]"
            )

    suggestions: list[str] = []
    catalog = set(problem_definition.categories if problem_definition is not None else [])
    if not catalog:
        catalog.update(category for _, category in CATEGORY_KEYWORDS)
    untried = sorted(category for category in catalog if category and category not in tried_categories)
    suggestions.extend(f"Try {category}." for category in untried[:4])
    suggestions.extend(
        f"Explore another variant of {category}."
        for category, records in sorted(categories.items())
        if category != "other" and len(records) <= 1
    )
    if keep:
        suggestions.append("Combine successful elements from the current best experiments.")
    if not suggestions:
        suggestions.append("Increase diversity across categories before doubling down on a single idea.")

    lines.extend(["", "### Promising directions"])
    lines.extend(f"- {suggestion}" for suggestion in suggestions[:6])
    return "\n".join(lines)
