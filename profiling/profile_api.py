import cProfile
import pstats
from pathlib import Path

import requests


BASE_URL = "http://127.0.0.1:8000"


def workload():

    for _ in range(100):

        response = requests.get(
            f"{BASE_URL}/health",
            timeout=5
        )

        response.raise_for_status()


def main():

    output_dir = Path(
        "profiling/reports"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    profile_path = (
        output_dir /
        "api_profile.prof"
    )

    profiler = cProfile.Profile()

    profiler.enable()

    workload()

    profiler.disable()

    profiler.dump_stats(
        str(profile_path)
    )

    stats = pstats.Stats(
        profiler
    )

    stats.sort_stats(
        "cumulative"
    )

    stats.print_stats(20)


if __name__ == "__main__":
    main()