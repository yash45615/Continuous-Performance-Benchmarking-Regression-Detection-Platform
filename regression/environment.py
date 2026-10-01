import hashlib
import json


IMPORTANT_KEYS = [
    "python_version",
    "platform",
    "processor",
    "cpu_count",
    "memory_total_mb"
]


def create_fingerprint(
    environment
):

    values = {
        key: environment.get(key)
        for key in IMPORTANT_KEYS
    }

    serialized = json.dumps(
        values,
        sort_keys=True
    )

    fingerprint = hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()

    return fingerprint


def compare_environments(
    first,
    second
):

    first_fingerprint = (
        create_fingerprint(first)
    )

    second_fingerprint = (
        create_fingerprint(second)
    )

    return {
        "match":
            first_fingerprint
            == second_fingerprint,

        "first":
            first_fingerprint,

        "second":
            second_fingerprint
    }