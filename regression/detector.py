from dataclasses import dataclass


@dataclass
class MetricComparison:
    metric: str
    baseline: float
    current: float
    change_percent: float
    threshold_percent: float
    regression: bool


def compare_latency(
    metric,
    baseline,
    current,
    threshold_percent=10.0
):
    if baseline <= 0:
        raise ValueError("Baseline must be greater than zero")

    change = ((current - baseline) / baseline) * 100

    return MetricComparison(
        metric=metric,
        baseline=baseline,
        current=current,
        change_percent=round(change, 2),
        threshold_percent=threshold_percent,
        regression=(change > threshold_percent)
    )


def compare_throughput(
    metric,
    baseline,
    current,
    threshold_percent=10.0
):
    if baseline <= 0:
        raise ValueError("Baseline must be greater than zero")

    change = ((current - baseline) / baseline) * 100

    return MetricComparison(
        metric=metric,
        baseline=baseline,
        current=current,
        change_percent=round(change, 2),
        threshold_percent=threshold_percent,
        regression=(change < -threshold_percent)
    )


def compare_metrics(
    baseline,
    current,
    threshold_percent=10.0
):
    comparisons = []

    latency_metrics = [
        "p50_ms",
        "p95_ms",
        "p99_ms"
    ]

    for metric in latency_metrics:
        if metric in baseline and metric in current:
            comparisons.append(
                compare_latency(
                    metric,
                    baseline[metric],
                    current[metric],
                    threshold_percent
                )
            )

    if "rps" in baseline and "rps" in current:
        comparisons.append(
            compare_throughput(
                "rps",
                baseline["rps"],
                current["rps"],
                threshold_percent
            )
        )

    return comparisons


def detect_regression(
    benchmark_name,
    baseline,
    current,
    threshold_percent=10.0
):
    if baseline <= 0:
        raise ValueError("Baseline must be greater than zero")

    change_percent = ((current - baseline) / baseline) * 100

    return MetricComparison(
        metric=benchmark_name,
        baseline=baseline,
        current=current,
        change_percent=round(change_percent, 2),
        threshold_percent=threshold_percent,
        regression=change_percent > threshold_percent
    )