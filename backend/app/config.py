from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root:
# D:\continuous-performance-platform
PROJECT_ROOT = Path(__file__).resolve().parents[2]

ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):

    database_url: str

    app_host: str = "127.0.0.1"

    app_port: int = 8000

    regression_threshold_percent: float = 10.0

    benchmark_iterations: int = 5

    baseline_runs: int = 5

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()