import json


def load_plan(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return data["plan"][0]["Plan"]


def analyze_plan(
    plan
):

    findings = []

    node_type = plan.get(
        "Node Type"
    )

    total_cost = plan.get(
        "Total Cost"
    )

    actual_time = plan.get(
        "Actual Total Time"
    )

    rows = plan.get(
        "Actual Rows"
    )

    if node_type:

        findings.append(
            f"Root node: {node_type}"
        )

    if total_cost is not None:

        findings.append(
            f"Estimated cost: {total_cost}"
        )

    if actual_time is not None:

        findings.append(
            f"Actual execution time: "
            f"{actual_time} ms"
        )

    if rows is not None:

        findings.append(
            f"Actual rows: {rows}"
        )

    if node_type == "Seq Scan":

        findings.append(
            "Sequential scan detected."
        )

    if node_type == "Index Scan":

        findings.append(
            "Index scan detected."
        )

    if node_type == "Index Only Scan":

        findings.append(
            "Index-only scan detected."
        )

    return findings