import json
from pathlib import Path

import statistics


def load_results(
    directory="data/results"
):

    files = Path(
        directory
    ).glob(
        "*.json"
    )

    results = []

    for file in files:

        try:

            data = json.loads(
                file.read_text(
                    encoding="utf-8"
                )
            )

            if "p95_ms" in data:

                results.append(
                    {
                        "file": file.name,
                        "p95_ms":
                            data["p95_ms"],
                        "p99_ms":
                            data["p99_ms"],
                        "rps":
                            data["rps"]
                    }
                )

        except Exception:

            continue

    return results


def main():

    results = load_results()

    if not results:

        print(
            "No benchmark results found."
        )

        return

    p95 = [
        item["p95_ms"]
        for item in results
    ]

    rps = [
        item["rps"]
        for item in results
    ]

    print(
        "========== PERFORMANCE TREND =========="
    )

    print(
        f"Runs: {len(results)}"
    )

    print(
        f"P95 average: "
        f"{statistics.mean(p95):.3f} ms"
    )

    print(
        f"P95 minimum: "
        f"{min(p95):.3f} ms"
    )

    print(
        f"P95 maximum: "
        f"{max(p95):.3f} ms"
    )

    print(
        f"RPS average: "
        f"{statistics.mean(rps):.3f}"
    )


if __name__ == "__main__":
    main()