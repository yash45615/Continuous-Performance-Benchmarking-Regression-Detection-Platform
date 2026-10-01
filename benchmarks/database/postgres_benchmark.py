import statistics
import time

from sqlalchemy import create_engine, text

import sys
from pathlib import Path

ROOT = Path(
    __file__
).resolve().parents[2]

sys.path.insert(
    0,
    str(ROOT / "backend")
)

from app.config import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True
)


QUERIES = {

    "lookup_product": """
        SELECT *
        FROM products
        WHERE id = 50000
    """,

    "category_aggregation": """
        SELECT
            category,
            COUNT(*),
            AVG(price)
        FROM products
        GROUP BY category
    """,

    "brand_aggregation": """
        SELECT
            brand,
            COUNT(*),
            AVG(price)
        FROM products
        GROUP BY brand
    """,

    "search": """
        SELECT *
        FROM products
        WHERE name ILIKE '%Laptop%'
        LIMIT 50
    """
}


def benchmark_query(
    query,
    iterations=10
):

    timings = []

    with engine.connect() as connection:

        for _ in range(iterations):

            start = time.perf_counter()

            connection.execute(
                text(query)
            ).fetchall()

            elapsed = (
                time.perf_counter()
                - start
            ) * 1000

            timings.append(
                elapsed
            )

    return {
        "min_ms":
            min(timings),

        "max_ms":
            max(timings),

        "mean_ms":
            statistics.mean(timings),

        "median_ms":
            statistics.median(timings),

        "p95_ms":
            sorted(timings)[
                min(
                    int(
                        len(timings)
                        * 0.95
                    ),
                    len(timings) - 1
                )
            ],

        "iterations":
            iterations
    }


def main():

    for name, query in QUERIES.items():

        print()
        print(
            f"Benchmarking: {name}"
        )

        result = benchmark_query(
            query
        )

        print(
            f"Mean: "
            f"{result['mean_ms']:.3f} ms"
        )

        print(
            f"Median: "
            f"{result['median_ms']:.3f} ms"
        )

        print(
            f"P95: "
            f"{result['p95_ms']:.3f} ms"
        )


if __name__ == "__main__":
    main()