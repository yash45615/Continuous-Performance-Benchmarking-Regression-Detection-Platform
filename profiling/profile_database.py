import json
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

ROOT = Path(
    __file__
).resolve().parents[1]

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

    "product_by_id": """
        SELECT *
        FROM products
        WHERE id = 50000
    """,

    "category_count": """
        SELECT category, COUNT(*)
        FROM products
        GROUP BY category
        ORDER BY COUNT(*) DESC
    """,

    "brand_average_price": """
        SELECT brand, AVG(price)
        FROM products
        GROUP BY brand
        ORDER BY AVG(price) DESC
    """,

    "search_products": """
        SELECT *
        FROM products
        WHERE name ILIKE '%Laptop%'
        LIMIT 50
    """
}


def explain_query(
    name,
    query
):

    explain = (
        "EXPLAIN "
        "(ANALYZE, BUFFERS, FORMAT JSON) "
        + query
    )

    with engine.connect() as connection:

        result = connection.execute(
            text(explain)
        )

        data = result.scalar()

    return {
        "name": name,
        "query": query,
        "plan": data
    }


def main():

    output_dir = Path(
        "profiling/reports"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    for name, query in QUERIES.items():

        print(
            f"Profiling: {name}"
        )

        result = explain_query(
            name,
            query
        )

        output_file = (
            output_dir /
            f"{name}_plan.json"
        )

        output_file.write_text(
            json.dumps(
                result,
                indent=2,
                default=str
            ),
            encoding="utf-8"
        )

        print(
            f"Saved: {output_file}"
        )


if __name__ == "__main__":
    main()