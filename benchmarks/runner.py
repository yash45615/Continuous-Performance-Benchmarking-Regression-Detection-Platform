import asyncio
import json
import statistics
import time
from pathlib import Path

import httpx
import psutil

from benchmarks.environment import (
    collect_environment
)


class BenchmarkRunner:

    def __init__(
        self,
        base_url="http://127.0.0.1:8000",
        concurrency=5,
        requests_per_worker=20
    ):

        self.base_url = base_url.rstrip("/")

        self.concurrency = concurrency

        self.requests_per_worker = (
            requests_per_worker
        )

    async def make_request(
        self,
        client,
        path
    ):

        start = time.perf_counter()

        try:

            response = await client.get(
                f"{self.base_url}{path}",
                timeout=30
            )

            elapsed = (
                time.perf_counter()
                - start
            ) * 1000

            return {
                "latency_ms": elapsed,
                "status_code": response.status_code,
                "success": (
                    response.status_code == 200
                )
            }

        except Exception as exc:

            elapsed = (
                time.perf_counter()
                - start
            ) * 1000

            return {
                "latency_ms": elapsed,
                "status_code": 0,
                "success": False,
                "error": str(exc)
            }

    async def worker(
        self,
        client,
        path
    ):

        results = []

        for _ in range(
            self.requests_per_worker
        ):

            result = await self.make_request(
                client,
                path
            )

            results.append(result)

        return results

    async def run_async(
        self,
        benchmark_name,
        path
    ):

        process = psutil.Process()

        start_time = time.perf_counter()

        async with httpx.AsyncClient() as client:

            tasks = []

            for _ in range(
                self.concurrency
            ):

                tasks.append(
                    self.worker(
                        client,
                        path
                    )
                )

            worker_results = await asyncio.gather(
                *tasks
            )

        elapsed_seconds = (
            time.perf_counter()
            - start_time
        )

        results = []

        for worker_result in worker_results:

            results.extend(
                worker_result
            )

        latencies = sorted(
            item["latency_ms"]
            for item in results
        )

        successful = [
            item
            for item in results
            if item["success"]
        ]

        errors = [
            item
            for item in results
            if not item["success"]
        ]

        if not latencies:

            raise RuntimeError(
                "No benchmark results collected"
            )

        def percentile(values, p):

            index = int(
                len(values) * p
            )

            index = min(
                index,
                len(values) - 1
            )

            return values[index]

        total_requests = len(results)

        rps = (
            total_requests
            / elapsed_seconds
        )

        cpu = process.cpu_percent(
            interval=0.2
        )

        memory_mb = (
            process.memory_info().rss
            / 1024
            / 1024
        )

        result = {
            "benchmark_name": benchmark_name,

            "timestamp": time.strftime(
                "%Y-%m-%dT%H:%M:%S"
            ),

            "total_requests":
                total_requests,

            "successful_requests":
                len(successful),

            "error_count":
                len(errors),

            "error_rate_percent":
                round(
                    len(errors)
                    / total_requests
                    * 100,
                    2
                ),

            "duration_seconds":
                round(
                    elapsed_seconds,
                    4
                ),

            "rps":
                round(
                    rps,
                    2
                ),

            "mean_ms":
                round(
                    statistics.mean(
                        latencies
                    ),
                    3
                ),

            "min_ms":
                round(
                    min(latencies),
                    3
                ),

            "max_ms":
                round(
                    max(latencies),
                    3
                ),

            "p50_ms":
                round(
                    percentile(
                        latencies,
                        0.50
                    ),
                    3
                ),

            "p95_ms":
                round(
                    percentile(
                        latencies,
                        0.95
                    ),
                    3
                ),

            "p99_ms":
                round(
                    percentile(
                        latencies,
                        0.99
                    ),
                    3
                ),

            "stddev_ms":
                round(
                    statistics.stdev(
                        latencies
                    )
                    if len(latencies) > 1
                    else 0,
                    3
                ),

            "cpu_percent":
                cpu,

            "memory_mb":
                round(
                    memory_mb,
                    2
                ),

            "environment":
                collect_environment()
        }

        return result

    def run(
        self,
        benchmark_name,
        path
    ):

        return asyncio.run(
            self.run_async(
                benchmark_name,
                path
            )
        )

    @staticmethod
    def save_result(
        result,
        path
    ):

        output = Path(path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                result,
                file,
                indent=2
            )