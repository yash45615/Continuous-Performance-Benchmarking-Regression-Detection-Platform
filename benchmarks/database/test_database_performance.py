import time

from sqlalchemy import create_engine, text

from backend.app.config import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True
)


def database_health_check():

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT 1")
        )

        return result.scalar()


def test_database_performance(benchmark):

    result = benchmark(
        database_health_check
    )

    assert result == 1