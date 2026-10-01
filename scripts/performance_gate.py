import sys

from regression.detector import (
    detect_regression
)


def main():

    baseline = float(
        input(
            "Enter baseline latency (ms): "
        )
    )

    current = float(
        input(
            "Enter current latency (ms): "
        )
    )

    threshold = 10.0

    result = detect_regression(
        benchmark_name="performance_gate",
        baseline=baseline,
        current=current,
        threshold_percent=threshold
    )

    print()
    print(
        f"Baseline: {result.baseline} ms"
    )

    print(
        f"Current: {result.current} ms"
    )

    print(
        f"Change: {result.change_percent}%"
    )

    print(
        f"Threshold: {result.threshold_percent}%"
    )

    if result.regression:

        print(
            "PERFORMANCE GATE: FAILED"
        )

        sys.exit(1)

    print(
        "PERFORMANCE GATE: PASSED"
    )


if __name__ == "__main__":
    main()