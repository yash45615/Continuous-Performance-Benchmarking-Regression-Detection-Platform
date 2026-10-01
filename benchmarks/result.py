from dataclasses import asdict, dataclass
from datetime import datetime
import json


@dataclass
class BenchmarkResult:

    benchmark_name: str

    timestamp: str

    duration_ms: float

    operations_per_second: float

    p50_ms: float | None = None

    p95_ms: float | None = None

    p99_ms: float | None = None

    cpu_percent: float | None = None

    memory_mb: float | None = None

    environment: dict | None = None

    commit_sha: str | None = None

    def to_dict(self):

        return asdict(self)

    def save(self, path):

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.to_dict(),
                file,
                indent=2
            )