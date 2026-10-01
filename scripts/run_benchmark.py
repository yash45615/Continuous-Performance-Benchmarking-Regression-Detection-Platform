import sys
from pathlib import Path

import yaml

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from benchmarks.runner import BenchmarkRunner


CONFIG_PATH = PROJECT_ROOT / "benchmarks" / "benchmark_config.yml"
RESULTS_DIR = PROJECT_ROOT / "data" / "results"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main():
    print("=" * 60)
    print("CONTINUOUS PERFORMANCE BENCHMARKING PLATFORM")
    print("=" * 60)
    print(f"Project root: {PROJECT_ROOT}")
    print()

    config = load_config()

    benchmark = config["benchmark"]

    benchmark_name = benchmark["name"]

    workload = next(
        item
        for item in config["workloads"]
        if item["name"] == benchmark_name
    )

    endpoint = workload["endpoint"]

    print(f"Benchmark       : {benchmark_name}")
    print(f"Endpoint        : {endpoint}")
    print(f"Iterations      : {benchmark['iterations']}")
    print(f"Warmup          : {benchmark['warmup_iterations']}")
    print(
        f"Regression      : "
        f"{benchmark['regression_threshold_percent']}%"
    )
    print()

    runner = BenchmarkRunner(
        base_url="http://127.0.0.1:8000",
        concurrency=5,
        requests_per_worker=benchmark["iterations"]
    )

    print("Running benchmark...")
    print()

    result = runner.run(
        benchmark_name,
        endpoint
    )

    output_path = (
        RESULTS_DIR
        / f"{benchmark_name}_latest.json"
    )

    BenchmarkRunner.save_result(
        result,
        output_path
    )

    print("=" * 60)
    print("BENCHMARK COMPLETE")
    print("=" * 60)

    print(f"Benchmark       : {result['benchmark_name']}")
    print(f"Total Requests  : {result['total_requests']}")
    print(f"Successful      : {result['successful_requests']}")
    print(f"Errors          : {result['error_count']}")
    print(f"Error Rate      : {result['error_rate_percent']}%")
    print(f"Duration        : {result['duration_seconds']} sec")
    print(f"RPS             : {result['rps']}")
    print()
    print(f"Mean            : {result['mean_ms']} ms")
    print(f"Min             : {result['min_ms']} ms")
    print(f"Max             : {result['max_ms']} ms")
    print(f"P50             : {result['p50_ms']} ms")
    print(f"P95             : {result['p95_ms']} ms")
    print(f"P99             : {result['p99_ms']} ms")
    print(f"Std Dev         : {result['stddev_ms']} ms")
    print()
    print(f"CPU             : {result['cpu_percent']}%")
    print(f"Memory          : {result['memory_mb']} MB")
    print()
    print(f"Result saved to : {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()