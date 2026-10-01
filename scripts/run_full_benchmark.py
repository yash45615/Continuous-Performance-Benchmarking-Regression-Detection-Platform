import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from benchmarks.runner import BenchmarkRunner

runner = BenchmarkRunner()
runner.run()


def run(
    command
):

    print()
    print(
        "================================"
    )

    print(
        "Running:",
        " ".join(command)
    )

    print(
        "================================"
    )

    result = subprocess.run(
        command
    )

    if result.returncode != 0:

        print(
            "Command failed."
        )

        sys.exit(
            result.returncode
        )


def main():

    run(
        [
            sys.executable,
            "scripts/run_repeated_benchmark.py",
            "--name",
            "product_list",
            "--path",
            "/products/?limit=50",
            "--runs",
            "5",
            "--concurrency",
            "5",
            "--requests",
            "20"
        ]
    )

    run(
        [
            sys.executable,
            "profiling/profile_database.py"
        ]
    )

    run(
        [
            sys.executable,
            "benchmarks/database/postgres_benchmark.py"
        ]
    )


if __name__ == "__main__":
    main()