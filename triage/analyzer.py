def analyze_regression(
    benchmark_name,
    change_percent,
    p95_change_percent=None
):

    reasons = []

    if change_percent > 20:

        reasons.append(
            "Large latency increase"
        )

    elif change_percent > 10:

        reasons.append(
            "Potential performance regression"
        )

    if (
        p95_change_percent is not None
        and p95_change_percent > 15
    ):

        reasons.append(
            "Tail latency degradation"
        )

    if not reasons:

        reasons.append(
            "No significant regression detected"
        )

    return {
        "benchmark": benchmark_name,
        "change_percent": change_percent,
        "p95_change_percent":
            p95_change_percent,
        "reasons": reasons
    }