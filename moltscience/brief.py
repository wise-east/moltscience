from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .query import load_index
from .schema import ExperimentStatus, MetricDirection


CATEGORY_KEYWORDS = [
    (("unroll", "loop"), "Loop optimization"),
    (("simd", "vector", "avx"), "Vectorization"),
    (("cache", "align", "prefetch"), "Memory optimization"),
    (("branch", "predict", "cmov"), "Branch optimization"),
    (("inline", "flatten"), "Function optimization"),
    (("lr", "learning rate"), "Learning rate tuning"),
    (("batch", "batch size"), "Batch size tuning"),
    (("arch", "layer", "hidden", "width", "depth"), "Architecture search"),
    (("optim", "adam", "sgd", "momentum"), "Optimizer tuning"),
    (("schedule", "warmup", "decay"), "Schedule tuning"),
]


def categorize(title: str, methodology: str) -> str:
    haystack = f"{title} {methodology}".lower()
    for keywords, category in CATEGORY_KEYWORDS:
        if any(keyword in haystack for keyword in keywords):
            return category
    return "Other"


def generate_brief(root: str | Path, problem: str) -> str:
    experiments = [record for record in load_index(root) if record["problem"] == problem]
    if not experiments:
        return f"## Research Brief: {problem}\n\nNo experiments found for {problem}."

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

    categories: dict[str, list[dict]] = defaultdict(list)
    tried_categories: set[str] = set()
    root_path = Path(root)
    for record in experiments:
        methodology = ""
        manifest_path = root_path / "experiments" / record["id"] / "manifest.json"
        if manifest_path.exists():
            import json

            methodology = json.loads(manifest_path.read_text()).get("methodology", "")
        category = categorize(record["title"], methodology)
        categories[category].append(record)
        tried_categories.add(category)

    lines = [
        f"## Research Brief: {problem}",
        best_line,
        f"Experiments: {len(experiments)} ({len(keep)} keep, {len(discard)} discard, {len(crash)} crash)",
        "",
        "### Approaches tried",
    ]
    for category, records in sorted(categories.items()):
        direction = records[0]["metric_direction"]
        best_record = sorted(
            records,
            key=lambda record: record["metric_value"],
            reverse=direction == MetricDirection.HIGHER_IS_BETTER.value,
        )[0]
        lines.append(
            f"- {category}: {len(records)} experiments, best={best_record['metric_value']} ({best_record['id']})"
        )
        for record in records[:3]:
            lines.append(
                f"  - {record['title']} → {record['metric_name']}={record['metric_value']} [{record['status']}]"
            )

    suggestions: list[str] = []
    all_categories = {category for _, category in CATEGORY_KEYWORDS}
    untried = sorted(all_categories - tried_categories)
    suggestions.extend(f"Try {category.lower()}." for category in untried[:3])
    suggestions.extend(
        f"Explore another variant of {category.lower()}."
        for category, records in sorted(categories.items())
        if len(records) == 1
    )
    if not suggestions:
        suggestions.append("Combine successful elements from the current best experiments.")

    lines.extend(["", "### Promising directions"])
    lines.extend(f"- {suggestion}" for suggestion in suggestions)
    return "\n".join(lines)
