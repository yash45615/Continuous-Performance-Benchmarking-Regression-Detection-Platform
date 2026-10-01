def determine_owner(
    benchmark_name
):

    name = benchmark_name.lower()

    if "database" in name or "db" in name:

        return {
            "team": "database-team",
            "component": "database"
        }

    if "api" in name:

        return {
            "team": "backend-team",
            "component": "api"
        }

    if "load" in name:

        return {
            "team": "performance-team",
            "component": "load-testing"
        }

    return {
        "team": "performance-team",
        "component": "unknown"
    }