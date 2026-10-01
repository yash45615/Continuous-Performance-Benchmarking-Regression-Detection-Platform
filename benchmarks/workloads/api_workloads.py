import random


WORKLOADS = [
    {
        "name": "product_list",
        "method": "GET",
        "path": "/products/?limit=50",
        "weight": 40
    },
    {
        "name": "product_detail",
        "method": "GET",
        "path": "/products/50000",
        "weight": 25
    },
    {
        "name": "product_search",
        "method": "GET",
        "path": "/products/search?q=Laptop",
        "weight": 20
    },
    {
        "name": "product_summary",
        "method": "GET",
        "path": "/products/summary",
        "weight": 10
    },
    {
        "name": "health",
        "method": "GET",
        "path": "/health",
        "weight": 5
    }
]


def choose_workload():

    values = [
        workload["name"]
        for workload in WORKLOADS
    ]

    weights = [
        workload["weight"]
        for workload in WORKLOADS
    ]

    selected = random.choices(
        values,
        weights=weights,
        k=1
    )[0]

    for workload in WORKLOADS:

        if workload["name"] == selected:

            return workload

    raise RuntimeError(
        "Workload not found"
    )