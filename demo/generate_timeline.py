from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "experiments"
OUT = Path(__file__).resolve().parent / "timeline.md"


def main() -> None:
    index = json.loads((ROOT / "index.json").read_text())
    records = sorted(index, key=lambda record: record["timestamp"])
    lines = ["# Experiment Timeline", ""]
    for record in records:
        summary_path = ROOT / "experiments" / record["id"] / "summary.md"
        summary = summary_path.read_text().strip().splitlines()
        methodology = summary[1] if len(summary) > 1 else "(no methodology)"
        lines.append(
            f"- **{record['timestamp']}** — `{record['agent']}` ran **{record['title']}** "
            f"on `{record['problem']}` → {record['metric_name']}={record['metric_value']} "
            f"[{record['status']}]  "
        )
        lines.append(f"  {methodology}")
        lines.append("")
    OUT.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
