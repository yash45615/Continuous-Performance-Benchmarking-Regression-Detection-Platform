from regression.detector import (
    compare_metrics
)


def test_latency_regression():

    baseline = {
        "p50_ms": 10,
        "p95_ms": 20,
        "p99_ms": 30,
        "rps": 100
    }

    current = {
        "p50_ms": 12,
        "p95_ms": 30,
        "p99_ms": 40,
        "rps": 95
    }

    comparisons = compare_metrics(
        baseline,
        current,
        threshold_percent=10
    )

    regressions = [
        item
        for item in comparisons
        if item.regression
    ]

    assert len(regressions) > 0