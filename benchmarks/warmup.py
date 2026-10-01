import time

import requests


def warmup(
    base_url,
    path,
    iterations=10
):

    print(
        f"Warming up {iterations} requests..."
    )

    for i in range(iterations):

        response = requests.get(
            f"{base_url}{path}",
            timeout=30
        )

        response.raise_for_status()

        print(
            f"Warmup {i + 1}/{iterations}",
            end="\r"
        )

        time.sleep(0.05)

    print()
    print(
        "Warmup completed."
    )