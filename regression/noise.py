import statistics


def calculate_cv(
    values
):

    if len(values) < 2:

        return 0

    mean = statistics.mean(
        values
    )

    if mean == 0:

        return 0

    standard_deviation = (
        statistics.stdev(values)
    )

    return (
        standard_deviation
        / mean
    )


def is_noisy(
    values,
    threshold=0.20
):

    cv = calculate_cv(
        values
    )

    return {
        "coefficient_of_variation": cv,
        "threshold": threshold,
        "noisy": cv > threshold
    }
if __name__ == "__main__":

    values = [
        100,
        102,
        98,
        101,
        99
    ]

    result = is_noisy(
        values
    )

    print(result)