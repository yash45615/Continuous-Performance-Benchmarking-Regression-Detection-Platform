import json


def load_plan(
    path
):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return data["plan"][0]["Plan"]


def compare_plans(
    baseline_path,
    current_path
):

    baseline = load_plan(
        baseline_path
    )

    current = load_plan(
        current_path
    )

    result = {

        "node_changed":
            baseline.get("Node Type")
            != current.get("Node Type"),

        "baseline_node":
            baseline.get("Node Type"),

        "current_node":
            current.get("Node Type"),

        "baseline_cost":
            baseline.get("Total Cost"),

        "current_cost":
            current.get("Total Cost"),

        "baseline_time":
            baseline.get(
                "Actual Total Time"
            ),

        "current_time":
            current.get(
                "Actual Total Time"
            )
    }

    return result