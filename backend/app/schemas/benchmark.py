from datetime import datetime

from pydantic import BaseModel


class BenchmarkCreate(BaseModel):
    benchmark_name: str
    environment: str

    commit_sha: str | None = None

    duration_ms: float
    operations_per_second: float | None = None

    p50_ms: float | None = None
    p95_ms: float | None = None
    p99_ms: float | None = None

    cpu_percent: float | None = None
    memory_mb: float | None = None

    status: str = "completed"

    metadata_json: str | None = None


class BenchmarkResponse(BenchmarkCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True