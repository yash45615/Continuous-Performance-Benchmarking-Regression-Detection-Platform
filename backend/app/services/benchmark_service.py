from sqlalchemy.orm import Session

from backend.app.models.benchmark import BenchmarkRun
from backend.app.schemas.benchmark import BenchmarkCreate


class BenchmarkService:

    @staticmethod
    def create(
        db: Session,
        benchmark: BenchmarkCreate
    ) -> BenchmarkRun:

        record = BenchmarkRun(
            benchmark_name=benchmark.benchmark_name,
            environment=benchmark.environment,
            commit_sha=benchmark.commit_sha,
            duration_ms=benchmark.duration_ms,
            operations_per_second=benchmark.operations_per_second,
            p50_ms=benchmark.p50_ms,
            p95_ms=benchmark.p95_ms,
            p99_ms=benchmark.p99_ms,
            cpu_percent=benchmark.cpu_percent,
            memory_mb=benchmark.memory_mb,
            status=benchmark.status,
            metadata_json=benchmark.metadata_json,
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return record

    @staticmethod
    def list_runs(
        db: Session,
        benchmark_name: str | None = None
    ):
        query = db.query(BenchmarkRun)

        if benchmark_name:
            query = query.filter(
                BenchmarkRun.benchmark_name == benchmark_name
            )

        return query.order_by(
            BenchmarkRun.created_at.desc()
        ).all()