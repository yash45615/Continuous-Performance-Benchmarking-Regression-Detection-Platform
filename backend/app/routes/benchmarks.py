from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.schemas.benchmark import (
    BenchmarkCreate,
    BenchmarkResponse,
)
from backend.app.services.benchmark_service import BenchmarkService


router = APIRouter(
    prefix="/benchmarks",
    tags=["Benchmarks"]
)


@router.post(
    "/",
    response_model=BenchmarkResponse
)
def create_benchmark(
    benchmark: BenchmarkCreate,
    db: Session = Depends(get_db)
):
    return BenchmarkService.create(
        db,
        benchmark
    )


@router.get(
    "/",
    response_model=list[BenchmarkResponse]
)
def get_benchmarks(
    benchmark_name: str | None = None,
    db: Session = Depends(get_db)
):
    return BenchmarkService.list_runs(
        db,
        benchmark_name
    )