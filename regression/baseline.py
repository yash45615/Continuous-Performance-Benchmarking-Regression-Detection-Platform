import json
from pathlib import Path


class BaselineManager:

    def __init__(
        self,
        directory="data/baselines"
    ):

        self.directory = Path(directory)

        self.directory.mkdir(
            parents=True,
            exist_ok=True
        )

    def save(
        self,
        benchmark_name,
        data
    ):

        path = (
            self.directory /
            f"{benchmark_name}.json"
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=2
            )

    def load(
        self,
        benchmark_name
    ):

        path = (
            self.directory /
            f"{benchmark_name}.json"
        )

        if not path.exists():

            return None

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)