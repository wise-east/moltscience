"""
Modal wrapper for running MoltScience experiments remotely.

Usage:
    # Run perf-takehome experiment
    python infra/modal_runner.py perf-takehome

    # Run tiny-mnist experiment
    python infra/modal_runner.py tiny-mnist

Requires: `modal token new` to authenticate before first use.
Fallback: if Modal is unavailable, experiments run locally (see PRD).
"""
import modal
import subprocess
import sys
import os

app = modal.App("moltscience-runner")

perf_image = modal.Image.debian_slim(python_version="3.12").pip_install("pytest")
mnist_image = modal.Image.debian_slim(python_version="3.12").pip_install("torch", "torchvision")


@app.function(image=perf_image, timeout=120, cpu=2)
def run_perf_takehome(solution_code: str) -> dict:
    """Run the perf-takehome solution on Modal and return results."""
    import tempfile, os, subprocess
    workdir = tempfile.mkdtemp()

    subprocess.run(
        ["git", "clone", "https://github.com/anthropics/original_performance_takehome", workdir],
        check=True, capture_output=True,
    )

    with open(os.path.join(workdir, "perf_takehome.py"), "w") as f:
        f.write(solution_code)

    result = subprocess.run(
        ["python", "tests/submission_tests.py"],
        cwd=workdir, capture_output=True, text=True, timeout=60,
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }


@app.function(image=mnist_image, timeout=180, cpu=4)
def run_tiny_mnist(train_code: str) -> dict:
    """Run the tiny-mnist training script on Modal and return results."""
    import tempfile, os, subprocess
    workdir = tempfile.mkdtemp()

    with open(os.path.join(workdir, "train.py"), "w") as f:
        f.write(train_code)

    result = subprocess.run(
        ["python", "train.py"],
        cwd=workdir, capture_output=True, text=True, timeout=150,
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }


@app.local_entrypoint()
def main(problem: str = "perf-takehome"):
    if problem == "perf-takehome":
        code_path = os.path.join(os.path.dirname(__file__), "..", "problems", "perf-takehome", "perf_takehome.py")
        with open(code_path) as f:
            code = f.read()
        result = run_perf_takehome.remote(code)
    elif problem == "tiny-mnist":
        code_path = os.path.join(os.path.dirname(__file__), "..", "problems", "tiny-mnist", "train.py")
        with open(code_path) as f:
            code = f.read()
        result = run_tiny_mnist.remote(code)
    else:
        print(f"Unknown problem: {problem}", file=sys.stderr)
        sys.exit(1)

    print(result["stdout"])
    if result["stderr"]:
        print(result["stderr"], file=sys.stderr)
    sys.exit(result["returncode"])
