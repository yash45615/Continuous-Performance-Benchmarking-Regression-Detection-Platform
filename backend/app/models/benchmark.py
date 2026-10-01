from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)

from backend.app.database import Base


class BenchmarkRun(Base):
    __tablename__ = "benchmark_runs"

    id = Column(Integer, primary_key=True, index=True)

    benchmark_name = Column(String(255), nullable=False)

    environment = Column(String(100), nullable=False)

    commit_sha = Column(String(100), nullable=True)

    duration_ms = Column(Float, nullable=False)

    operations_per_second = Column(Float, nullable=True)

    p50_ms = Column(Float, nullable=True)
    p95_ms = Column(Float, nullable=True)
    p99_ms = Column(Float, nullable=True)

    cpu_percent = Column(Float, nullable=True)
    memory_mb = Column(Float, nullable=True)

    status = Column(String(50), default="completed")

    metadata_json = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )