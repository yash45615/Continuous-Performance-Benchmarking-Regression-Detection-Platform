from triage.router import determine_owner
from triage.analyzer import analyze_regression


def triage(
    benchmark_name,
    change_percent,
    p95_change_percent
):

    owner = determine_owner(
        benchmark_name
    )

    analysis = analyze_regression(
        benchmark_name,
        change_percent,
        p95_change_percent
    )

    return {
        "owner": owner,
        "analysis": analysis
    }