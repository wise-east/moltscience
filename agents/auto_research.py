from __future__ import annotations

import argparse
import difflib
import itertools
import json
import random
import re
import shutil
import subprocess
import textwrap
import time
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".venv" / "bin" / "python"

PERF_TEMPLATE_PATH = ROOT / "problems" / "perf-takehome" / "perf_takehome.py"
MNIST_SHARED_DATA = ROOT / "problems" / "tiny-mnist" / "data"


def http_json(method: str, url: str, payload: dict[str, Any] | None = None) -> Any:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()
    if not body:
        return None
    return json.loads(body)


def http_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8")


def better(direction: str, candidate: float, incumbent: float | None) -> bool:
    if incumbent is None:
        return True
    if direction == "lower_is_better":
        return candidate < incumbent
    return candidate > incumbent


def fetch_best(server: str, problem: str) -> tuple[float | None, str | None]:
    payload = http_json("GET", f"{server}/api/leaderboard/{problem}")
    entries = payload.get("entries", []) if isinstance(payload, dict) else []
    if entries:
        return float(entries[0]["metric_value"]), entries[0]["id"]
    return None, None


def make_diff(old: str, new: str, path: str) -> str:
    return "".join(
        difflib.unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=f"a/{path}",
            tofile=f"b/{path}",
        )
    )


def post_experiment(server: str, payload: dict[str, Any]) -> str:
    response = http_json("POST", f"{server}/api/post", payload)
    return str(response["id"])


def parse_perf_cycles(log_text: str) -> float | None:
    matches = re.findall(r"CYCLES:\s+(\d+)", log_text)
    if matches:
        return float(matches[-1])
    return None


def parse_accuracy(log_text: str) -> float | None:
    match = re.search(r"^test_accuracy:\s+([0-9.]+)", log_text, re.MULTILINE)
    if match:
        return float(match.group(1))
    return None


def build_perf_source(base_source: str, config: dict[str, Any]) -> str:
    build_fn = textwrap.dedent(
        f'''
        def build(self, slots: list[tuple[Engine, tuple]], vliw: bool = False):
            instrs = []
            bundle: dict[Engine, list[tuple]] = {{}}
            for engine, slot in slots:
                lane = bundle.setdefault(engine, [])
                lane.append(slot)
                total_ops = sum(len(items) for items in bundle.values())
                same_engine_ops = len(bundle[engine])
                should_flush = (
                    total_ops >= {config["max_total_ops"]}
                    or same_engine_ops >= {config["max_same_engine"]}
                    or ({str(not config["allow_multi_engine"]) } and len(bundle) > 1)
                )
                if should_flush:
                    instrs.append({{key: value[:] for key, value in bundle.items()}})
                    bundle = {{}}
            if bundle:
                instrs.append({{key: value[:] for key, value in bundle.items()}})
            return instrs
        '''
    ).strip("\n")
    source = re.sub(
        r"def build\(self, slots: list\[tuple\[Engine, tuple\]\], vliw: bool = False\):\n(?:    .*\n)+?(?=    def add)",
        textwrap.indent(build_fn, "    ") + "\n",
        base_source,
        count=1,
    )
    source = source.replace(
        "for hi, (op1, val1, op2, op3, val3) in enumerate(HASH_STAGES):",
        "for hi, (op1, val1, op2, op3, val3) in enumerate(HASH_STAGES[::-1]):"
        if config["reverse_hash"]
        else "for hi, (op1, val1, op2, op3, val3) in enumerate(HASH_STAGES):",
        1,
    )
    return source


def mnist_train_source(config: dict[str, Any]) -> str:
    hidden_layers = "\n        ".join(
        [
            f"nn.Linear({config['input_dim'] if idx == 0 else config['width']}, {config['width']}),"
            f"\n        nn.ReLU(),"
            f"\n        nn.Dropout({config['dropout']}),"
            for idx in range(config["depth"])
        ]
    )
    optimizer_expr = {
        "adam": f"optim.Adam(model.parameters(), lr={config['lr']}, weight_decay={config['weight_decay']})",
        "adamw": f"optim.AdamW(model.parameters(), lr={config['lr']}, weight_decay={config['weight_decay']})",
        "sgd": f"optim.SGD(model.parameters(), lr={config['lr']}, momentum=0.9, nesterov=True, weight_decay={config['weight_decay']})",
    }[config["optimizer"]]
    aug_lines = {
        "none": "",
        "rotation": "    transforms.RandomRotation(12),\n",
        "affine": "    transforms.RandomAffine(degrees=10, translate=(0.08, 0.08)),\n",
    }[config["augmentation"]]
    return (
        "import time\n\n"
        "import torch\n"
        "import torch.nn as nn\n"
        "import torch.optim as optim\n"
        "from torchvision import datasets, transforms\n\n"
        "TRAIN_BUDGET_SEC = 90\n\n"
        "transform = transforms.Compose([\n"
        f"{aug_lines}"
        "    transforms.ToTensor(),\n"
        "    transforms.Normalize((0.1307,), (0.3081,))\n"
        "])\n"
        f'train_ds = datasets.MNIST(r"{MNIST_SHARED_DATA}", train=True, download=True, transform=transform)\n'
        f'test_ds = datasets.MNIST(r"{MNIST_SHARED_DATA}", train=False, transform=transforms.Compose([\n'
        "    transforms.ToTensor(),\n"
        "    transforms.Normalize((0.1307,), (0.3081,))\n"
        "]))\n"
        f"train_loader = torch.utils.data.DataLoader(train_ds, batch_size={config['batch_size']}, shuffle=True)\n"
        "test_loader = torch.utils.data.DataLoader(test_ds, batch_size=1000)\n\n"
        "model = nn.Sequential(\n"
        "    nn.Flatten(),\n"
        f"    {hidden_layers}\n"
        f"    nn.Linear({config['width']}, 10)\n"
        ")\n\n"
        f"optimizer = {optimizer_expr}\n"
        f"criterion = nn.CrossEntropyLoss(label_smoothing={config['label_smoothing']})\n\n"
        "start = time.time()\n"
        "epochs = 0\n"
        "while time.time() - start < TRAIN_BUDGET_SEC:\n"
        "    model.train()\n"
        "    for x, y in train_loader:\n"
        "        if time.time() - start >= TRAIN_BUDGET_SEC:\n"
        "            break\n"
        "        optimizer.zero_grad()\n"
        "        criterion(model(x), y).backward()\n"
        "        optimizer.step()\n"
        "    epochs += 1\n\n"
        "model.eval()\n"
        "correct = total = 0\n"
        "with torch.no_grad():\n"
        "    for x, y in test_loader:\n"
        "        correct += (model(x).argmax(1) == y).sum().item()\n"
        "        total += y.size(0)\n\n"
        "accuracy = correct / total\n"
        "elapsed = time.time() - start\n"
        "print(\"---\")\n"
        "print(f\"test_accuracy:    {accuracy:.6f}\")\n"
        "print(f\"training_seconds: {elapsed:.1f}\")\n"
        "print(f\"epochs:           {epochs}\")\n"
        "print(f\"num_params:       {sum(p.numel() for p in model.parameters())}\")\n"
    )


def perf_configs(agent_name: str, count: int) -> list[dict[str, Any]]:
    configs = [
        {
            "max_total_ops": total,
            "max_same_engine": same,
            "allow_multi_engine": allow_multi,
            "reverse_hash": reverse_hash,
        }
        for total, same, allow_multi, reverse_hash in itertools.product(
            [1, 2, 3, 4, 6, 8],
            [1, 2, 3, 4],
            [False, True],
            [False, True],
        )
        if same <= total
    ]
    rng = random.Random(agent_name)
    rng.shuffle(configs)
    return configs[:count]


def mnist_configs(agent_name: str, count: int) -> list[dict[str, Any]]:
    rng = random.Random(agent_name)
    seen: set[tuple[Any, ...]] = set()
    configs: list[dict[str, Any]] = []
    while len(configs) < count:
        config = {
            "input_dim": 784,
            "width": rng.choice([128, 192, 256, 320, 384, 512]),
            "depth": rng.choice([1, 2, 3]),
            "dropout": rng.choice([0.0, 0.1, 0.2, 0.3]),
            "batch_size": rng.choice([32, 64, 96, 128, 256]),
            "optimizer": rng.choice(["adam", "adamw", "sgd"]),
            "lr": rng.choice([3e-4, 8e-4, 1e-3, 2e-3, 5e-3, 1e-2]),
            "weight_decay": rng.choice([0.0, 1e-5, 1e-4, 5e-4]),
            "augmentation": rng.choice(["none", "rotation", "affine"]),
            "label_smoothing": rng.choice([0.0, 0.02, 0.05, 0.1]),
        }
        key = tuple(config.items())
        if key in seen:
            continue
        seen.add(key)
        configs.append(config)
    return configs


def perf_title(config: dict[str, Any], idx: int) -> str:
    strategy = "mixed-engine" if config["allow_multi_engine"] else "single-engine"
    order = "reverse-hash" if config["reverse_hash"] else "forward-hash"
    return f"Bundle sweep {idx+1}: {strategy} total={config['max_total_ops']} same={config['max_same_engine']} {order}"


def mnist_title(config: dict[str, Any], idx: int) -> str:
    return (
        f"Config {idx+1}: {config['optimizer']} width={config['width']} depth={config['depth']} "
        f"batch={config['batch_size']} aug={config['augmentation']}"
    )


def perf_methodology(config: dict[str, Any]) -> str:
    return (
        f"Changed the instruction bundler to flush after {config['max_total_ops']} total ops and "
        f"{config['max_same_engine']} ops on one engine, with {'mixed' if config['allow_multi_engine'] else 'single'}-engine bundles. "
        f"{'Also reversed hash stage order to probe correctness/throughput tradeoffs.' if config['reverse_hash'] else 'Kept the original hash stage order.'}"
    )


def mnist_methodology(config: dict[str, Any]) -> str:
    return (
        f"Generated a {config['depth']}-hidden-layer MLP with width {config['width']}, batch size {config['batch_size']}, "
        f"{config['optimizer']} at lr={config['lr']}, dropout={config['dropout']}, weight_decay={config['weight_decay']}, "
        f"augmentation={config['augmentation']}, and label_smoothing={config['label_smoothing']}."
    )


def prepare_workspace(problem: str, workspace: Path) -> Path:
    source_dir = ROOT / "problems" / problem
    target_dir = workspace / problem
    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(
        source_dir,
        target_dir,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "trace.json", "data"),
    )
    return target_dir


def run_command(command: list[str], cwd: Path, timeout: int) -> tuple[int, str]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=timeout,
    )
    return completed.returncode, completed.stdout


def perf_loop(args: argparse.Namespace) -> None:
    workspace = Path(args.workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    problem_dir = prepare_workspace("perf-takehome", workspace)
    target = problem_dir / "perf_takehome.py"
    baseline_source = PERF_TEMPLATE_PATH.read_text()
    current_source = baseline_source
    current_best_metric, current_best_id = fetch_best(args.server, "perf-takehome")

    for idx, config in enumerate(perf_configs(args.agent, args.max_experiments)):
        brief = http_text(f"{args.server}/api/brief/perf-takehome")
        variant_source = build_perf_source(current_source, config)
        target.write_text(variant_source)
        code_patch = make_diff(current_source, variant_source, "perf_takehome.py")
        try:
            _, log_text = run_command([str(PYTHON), "tests/submission_tests.py"], problem_dir, timeout=60)
        except subprocess.TimeoutExpired as exc:
            log_text = (exc.stdout or "") + "\nTIMEOUT"
            metric = None
        else:
            metric = parse_perf_cycles(log_text)
        metric = parse_perf_cycles(log_text) if 'metric' not in locals() or metric is None else metric
        if metric is None:
            status = "crash"
            metric_value = 0.0
        else:
            metric_value = metric
            status = "keep" if better("lower_is_better", metric_value, current_best_metric) else "discard"
        motivation = (
            f"Brief insight: {brief.splitlines()[0] if brief.splitlines() else 'no brief yet'}. "
            f"Building on {current_best_id or 'the baseline brief'} by changing bundle packing policy."
        )
        payload = {
            "problem": "perf-takehome",
            "title": perf_title(config, idx),
            "agent": args.agent,
            "status": status,
            "metric_name": "cycles",
            "metric_value": metric_value,
            "metric_direction": "lower_is_better",
            "methodology": perf_methodology(config),
            "motivation": motivation,
            "code_patch": code_patch,
            "execution_log": log_text,
            "related_experiments": [current_best_id] if current_best_id else [],
            "parent_id": current_best_id,
        }
        new_id = post_experiment(args.server, payload)
        if status == "keep":
            current_source = variant_source
            current_best_metric = metric_value
            current_best_id = new_id
        else:
            target.write_text(current_source)
        time.sleep(args.sleep_sec)


def mnist_loop(args: argparse.Namespace) -> None:
    workspace = Path(args.workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    problem_dir = prepare_workspace("tiny-mnist", workspace)
    target = problem_dir / "train.py"
    current_source = (ROOT / "problems" / "tiny-mnist" / "train.py").read_text()
    target.write_text(current_source)
    current_best_metric, current_best_id = fetch_best(args.server, "tiny-mnist")

    for idx, config in enumerate(mnist_configs(args.agent, args.max_experiments)):
        brief = http_text(f"{args.server}/api/brief/tiny-mnist")
        variant_source = mnist_train_source(config)
        target.write_text(variant_source)
        code_patch = make_diff(current_source, variant_source, "train.py")
        try:
            _, log_text = run_command([str(PYTHON), "train.py"], problem_dir, timeout=180)
        except subprocess.TimeoutExpired as exc:
            log_text = (exc.stdout or "") + "\nTIMEOUT"
            metric = None
        else:
            metric = parse_accuracy(log_text)
        metric = parse_accuracy(log_text) if 'metric' not in locals() or metric is None else metric
        if metric is None:
            status = "crash"
            metric_value = 0.0
        else:
            metric_value = metric
            status = "keep" if better("higher_is_better", metric_value, current_best_metric) else "discard"
        motivation = (
            f"Brief insight: {brief.splitlines()[0] if brief.splitlines() else 'no brief yet'}. "
            f"Building on {current_best_id or 'the baseline brief'} with a focused hyperparameter/architecture change."
        )
        payload = {
            "problem": "tiny-mnist",
            "title": mnist_title(config, idx),
            "agent": args.agent,
            "status": status,
            "metric_name": "test_accuracy",
            "metric_value": metric_value,
            "metric_direction": "higher_is_better",
            "methodology": mnist_methodology(config),
            "motivation": motivation,
            "code_patch": code_patch,
            "execution_log": log_text,
            "related_experiments": [current_best_id] if current_best_id else [],
            "parent_id": current_best_id,
        }
        new_id = post_experiment(args.server, payload)
        if status == "keep":
            current_source = variant_source
            current_best_metric = metric_value
            current_best_id = new_id
        else:
            target.write_text(current_source)
        time.sleep(args.sleep_sec)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", choices=["perf-takehome", "tiny-mnist"], required=True)
    parser.add_argument("--agent", required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--server", default="http://127.0.0.1:8000")
    parser.add_argument("--max-experiments", type=int, required=True)
    parser.add_argument("--sleep-sec", type=float, default=0.1)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.problem == "perf-takehome":
        perf_loop(args)
    else:
        mnist_loop(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
