from fastapi import FastAPI
from prometheus_fastapi_instrumentator import (
    Instrumentator
)

from backend.app.database import Base, engine
from backend.app.models import BenchmarkRun, Product
from backend.app.routes.benchmarks import (
    router as benchmark_router
)
from backend.app.routes.products import (
    router as product_router
)


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Continuous Performance Benchmarking Platform",
    description=(
        "Continuous benchmarking, profiling, "
        "regression detection and performance triage."
    ),
    version="3.0.0"
)


app.include_router(
    benchmark_router
)

app.include_router(
    product_router
)


@app.get("/")
def root():

    return {
        "name":
            "Continuous Performance Benchmarking Platform",
        "version": "3.0.0",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


Instrumentator().instrument(
    app
).expose(
    app
)