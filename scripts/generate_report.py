import json
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from reports.generator import generate_report


def load_latest_result():
    results_dir = PROJECT_ROOT / "data" / "results"

    result_files = sorted(
        results_dir.glob("*.json"),
        key=lambda file: file.stat().st_mtime,
        reverse=True
    )

    if not result_files:
        raise FileNotFoundError(
            "No benchmark result JSON files found in data/results"
        )

    latest_file = result_files[0]

    with latest_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return latest_file, data


def main():
    result_file, current = load_latest_result()

    benchmark_name = current["benchmark_name"]

    baseline = {
        "available": False,
        "message": "No baseline comparison available for this report."
    }

    comparisons = []

    triage = {
        "status": "No regression analysis available",
        "message": "This report contains the latest benchmark measurements."
    }

    output_file = (
        PROJECT_ROOT
        / "reports"
        / "generated"
        / f"{benchmark_name}_performance_report.html"
    )

    report_path = generate_report(
        benchmark_name=benchmark_name,
        baseline=baseline,
        current=current,
        comparisons=comparisons,
        triage=triage,
        output_file=output_file
    )

    print()
    print("=" * 60)
    print("PERFORMANCE REPORT GENERATED")
    print("=" * 60)
    print(f"Benchmark : {benchmark_name}")
    print(f"Input     : {result_file}")
    print(f"Report    : {report_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()