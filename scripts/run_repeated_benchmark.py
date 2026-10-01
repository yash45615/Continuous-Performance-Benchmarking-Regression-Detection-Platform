import sys
from pathlib import Path

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse
import json
import statistics

from benchmarks.runner import BenchmarkRunner
from benchmarks.warmup import warmup


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--name",
        required=True
    )

    parser.add_argument(
        "--path",
        required=True
    )

    parser.add_argument(
        "--runs",
        type=int,
        default=5
    )

    parser.add_argument(
        "--concurrency",
        type=int,
        default=5
    )

    parser.add_argument(
        "--requests",
        type=int,
        default=20
    )

    args = parser.parse_args()

    base_url = (
        "http://127.0.0.1:8000"
    )

    print("=" * 60)
    print("CONTINUOUS PERFORMANCE BENCHMARK")
    print("=" * 60)

    print(
        f"Benchmark: {args.name}"
    )

    print(
        f"Endpoint: {args.path}"
    )

    print(
        f"Runs: {args.runs}"
    )

    print(
        f"Concurrency: {args.concurrency}"
    )

    print(
        f"Requests per worker: {args.requests}"
    )

    print()

    warmup(
        base_url,
        args.path,
        10
    )

    runner = BenchmarkRunner(
        base_url=base_url,
        concurrency=args.concurrency,
        requests_per_worker=args.requests
    )

    results = []

    for run_number in range(
        1,
        args.runs + 1
    ):

        print(
            f"\nRun {run_number}/{args.runs}"
        )

        result = runner.run(
            benchmark_name=args.name,
            path=args.path
        )

        results.append(result)

        print(
            f"Requests: "
            f"{result['total_requests']}"
        )

        print(
            f"Successful: "
            f"{result['successful_requests']}"
        )

        print(
            f"Errors: "
            f"{result['error_count']}"
        )

        print(
            f"P50: "
            f"{result['p50_ms']} ms"
        )

        print(
            f"P95: "
            f"{result['p95_ms']} ms"
        )

        print(
            f"P99: "
            f"{result['p99_ms']} ms"
        )

        print(
            f"RPS: "
            f"{result['rps']}"
        )

    p95_values = [
        result["p95_ms"]
        for result in results
    ]

    p99_values = [
        result["p99_ms"]
        for result in results
    ]

    rps_values = [
        result["rps"]
        for result in results
    ]

    summary = {

        "benchmark_name":
            args.name,

        "runs":
            args.runs,

        "configuration": {
            "concurrency":
                args.concurrency,

            "requests_per_worker":
                args.requests,

            "total_requests_per_run":
                (
                    args.concurrency
                    * args.requests
                )
        },

        "p95": {

            "mean":
                statistics.mean(
                    p95_values
                ),

            "median":
                statistics.median(
                    p95_values
                ),

            "min":
                min(p95_values),

            "max":
                max(p95_values),

            "stddev":
                (
                    statistics.stdev(
                        p95_values
                    )
                    if len(p95_values) > 1
                    else 0
                )
        },

        "p99": {

            "mean":
                statistics.mean(
                    p99_values
                ),

            "median":
                statistics.median(
                    p99_values
                ),

            "min":
                min(p99_values),

            "max":
                max(p99_values),

            "stddev":
                (
                    statistics.stdev(
                        p99_values
                    )
                    if len(p99_values) > 1
                    else 0
                )
        },

        "rps": {

            "mean":
                statistics.mean(
                    rps_values
                ),

            "median":
                statistics.median(
                    rps_values
                ),

            "min":
                min(rps_values),

            "max":
                max(rps_values),

            "stddev":
                (
                    statistics.stdev(
                        rps_values
                    )
                    if len(rps_values) > 1
                    else 0
                )
        },

        "individual_runs":
            results
    }

    output_dir = Path(
        "data/results"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_dir /
        f"{args.name}_summary.json"
    )

    output_file.write_text(
        json.dumps(
            summary,
            indent=2
        ),
        encoding="utf-8"
    )

    print()

    print(
        "========== SUMMARY =========="
    )

    print(
        f"P95 median: "
        f"{summary['p95']['median']:.3f} ms"
    )

    print(
        f"P95 stddev: "
        f"{summary['p95']['stddev']:.3f} ms"
    )

    print(
        f"P99 median: "
        f"{summary['p99']['median']:.3f} ms"
    )

    print(
        f"P99 stddev: "
        f"{summary['p99']['stddev']:.3f} ms"
    )

    print(
        f"RPS median: "
        f"{summary['rps']['median']:.3f}"
    )

    print(
        f"RPS stddev: "
        f"{summary['rps']['stddev']:.3f}"
    )

    print(
        f"Saved: {output_file}"
    )


if __name__ == "__main__":
    main()