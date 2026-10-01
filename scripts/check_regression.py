import argparse
import json
import sys
from pathlib import Path

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from regression.detector import compare_metrics


def main():

    parser = argparse.ArgumentParser(
        description="Compare benchmark results against a baseline."
    )

    parser.add_argument(
        "--baseline",
        required=True
    )

    parser.add_argument(
        "--current",
        required=True
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=10.0
    )

    args = parser.parse_args()

    with open(
        args.baseline,
        "r",
        encoding="utf-8"
    ) as file:

        baseline = json.load(file)

    with open(
        args.current,
        "r",
        encoding="utf-8"
    ) as file:

        current = json.load(file)

    comparisons = compare_metrics(
        baseline,
        current,
        args.threshold
    )

    regression_found = False

    print()
    print("=" * 60)
    print("REGRESSION CHECK")
    print("=" * 60)
    print()

    print(
        f"Baseline : {args.baseline}"
    )

    print(
        f"Current  : {args.current}"
    )

    print(
        f"Threshold: {args.threshold}%"
    )

    print()

    for comparison in comparisons:

        status = (
            "REGRESSION"
            if comparison.regression
            else "PASS"
        )

        print(
            f"{comparison.metric}: "
            f"{comparison.baseline} -> "
            f"{comparison.current} | "
            f"{comparison.change_percent}% | "
            f"{status}"
        )

        if comparison.regression:
            regression_found = True

    print()

    if regression_found:

        print("=" * 60)
        print("PERFORMANCE GATE FAILED")
        print("=" * 60)

        sys.exit(1)

    print("=" * 60)
    print("PERFORMANCE GATE PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()