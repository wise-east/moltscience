from __future__ import annotations

import json
import subprocess
import sys

from moltscience import MoltScience
from moltscience.web import create_app


def test_post_creates_experiment_dir_with_manifest(tmp_path):
    store = MoltScience(str(tmp_path / "experiments"))
    exp_id = store.post(
        problem="perf-takehome",
        title="Baseline: unoptimized",
        agent="setup",
        status="keep",
        metric_name="cycles",
        metric_value=147048,
        metric_direction="lower_is_better",
        methodology="Original code.",
    )
    exp_dir = tmp_path / "experiments" / "experiments" / exp_id
    assert exp_dir.exists()
    manifest = json.loads((exp_dir / "manifest.json").read_text())
    assert manifest["title"] == "Baseline: unoptimized"
    assert (tmp_path / "experiments" / "index.json").exists()
    assert (tmp_path / "experiments" / "leaderboard.json").exists()


def test_query_returns_posted_experiments_filtered_by_problem(tmp_path):
    store = MoltScience(str(tmp_path / "experiments"))
    store.post(
        problem="perf-takehome",
        title="Perf baseline",
        agent="setup",
        status="keep",
        metric_name="cycles",
        metric_value=100.0,
        metric_direction="lower_is_better",
    )
    store.post(
        problem="tiny-mnist",
        title="MNIST baseline",
        agent="setup",
        status="keep",
        metric_name="test_accuracy",
        metric_value=0.9,
        metric_direction="higher_is_better",
    )
    results = store.query(problem="perf-takehome")
    assert len(results) == 1
    assert results[0]["problem"] == "perf-takehome"


def test_get_levels_include_expected_fields(tmp_path):
    store = MoltScience(str(tmp_path / "experiments"))
    exp_id = store.post(
        problem="tiny-mnist",
        title="Add motivation",
        agent="agent-1",
        status="discard",
        metric_name="test_accuracy",
        metric_value=0.91,
        metric_direction="higher_is_better",
        methodology="Tweaked model width.",
        motivation="Wider hidden layers may help.",
    )
    level0 = store.get(exp_id, level=0)
    level2 = store.get(exp_id, level=2)
    assert level0["title"] == "Add motivation"
    assert "motivation" not in level0
    assert level2["motivation"] == "Wider hidden layers may help."


def test_leaderboard_returns_sorted_results(tmp_path):
    store = MoltScience(str(tmp_path / "experiments"))
    store.post(
        problem="perf-takehome",
        title="Slow",
        agent="a",
        status="keep",
        metric_name="cycles",
        metric_value=200.0,
        metric_direction="lower_is_better",
    )
    best_id = store.post(
        problem="perf-takehome",
        title="Fast",
        agent="b",
        status="keep",
        metric_name="cycles",
        metric_value=100.0,
        metric_direction="lower_is_better",
    )
    leaderboard = store.leaderboard("perf-takehome")
    assert leaderboard["entries"][0]["id"] == best_id


def test_brief_mentions_problem(tmp_path):
    store = MoltScience(str(tmp_path / "experiments"))
    store.post(
        problem="tiny-mnist",
        title="Baseline",
        agent="setup",
        status="keep",
        metric_name="test_accuracy",
        metric_value=0.95,
        metric_direction="higher_is_better",
        methodology="Initial Adam baseline.",
    )
    brief = store.brief("tiny-mnist")
    assert brief
    assert "tiny-mnist" in brief


def test_cli_post_and_query_round_trip(tmp_path):
    root = tmp_path / "experiments"
    post = subprocess.run(
        [
            sys.executable,
            "-m",
            "moltscience",
            "post",
            "--root",
            str(root),
            "--problem",
            "perf-takehome",
            "--title",
            "CLI baseline",
            "--agent",
            "cli",
            "--status",
            "keep",
            "--metric-name",
            "cycles",
            "--metric-value",
            "123",
            "--metric-direction",
            "lower_is_better",
            "--methodology",
            "CLI smoke test.",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "exp-" in post.stdout
    query = subprocess.run(
        [
            sys.executable,
            "-m",
            "moltscience",
            "query",
            "--root",
            str(root),
            "--problem",
            "perf-takehome",
            "--level",
            "0",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "CLI baseline" in query.stdout


def test_web_homepage_and_experiment_detail_render(tmp_path):
    store = MoltScience(str(tmp_path / "experiments"))
    exp_id = store.post(
        problem="perf-takehome",
        title="Web baseline",
        agent="setup",
        status="keep",
        metric_name="cycles",
        metric_value=111.0,
        metric_direction="lower_is_better",
        methodology="Web smoke test.",
        motivation="Exercise the Flask UI.",
    )
    app = create_app(str(tmp_path / "experiments"))
    client = app.test_client()
    home = client.get("/")
    assert home.status_code == 200
    assert "MoltScience Experiment Feed" in home.get_data(as_text=True)
    detail = client.get(f"/e/{exp_id}")
    assert detail.status_code == 200
    assert "Web baseline" in detail.get_data(as_text=True)
