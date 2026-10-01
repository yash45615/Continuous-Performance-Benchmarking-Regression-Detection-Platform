import statistics


def calculate_variance(values):

    if len(values) < 2:
        return 0.0

    return statistics.variance(values)


def calculate_standard_deviation(values):

    if len(values) < 2:
        return 0.0

    return statistics.stdev(values)


def calculate_mean(values):

    if not values:
        raise ValueError(
            "Values cannot be empty"
        )

    return statistics.mean(values)


def coefficient_of_variation(values):

    mean = calculate_mean(values)

    if mean == 0:
        return 0.0

    std = calculate_standard_deviation(
        values
    )

    return std / mean