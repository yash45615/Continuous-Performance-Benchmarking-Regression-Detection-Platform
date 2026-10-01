from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)

from backend.app.database import Base


class BenchmarkMetric(Base):

    __tablename__ = "benchmark_metrics"

    id = Column(
        Integer,
        primary_key=True
    )

    benchmark_run_id = Column(
        Integer,
        ForeignKey(
            "benchmark_runs.id"
        ),
        nullable=False
    )

    metric_name = Column(
        String(100),
        nullable=False
    )

    metric_value = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )