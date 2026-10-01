from regression.variance import (
    calculate_mean,
    calculate_standard_deviation,
    calculate_variance,
    coefficient_of_variation,
)


def test_mean():

    values = [100, 110, 90]

    assert calculate_mean(values) == 100


def test_variance():

    values = [100, 110, 90]

    assert calculate_variance(values) > 0


def test_standard_deviation():

    values = [100, 110, 90]

    assert (
        calculate_standard_deviation(values)
        > 0
    )


def test_coefficient_of_variation():

    values = [100, 110, 90]

    assert (
        coefficient_of_variation(values)
        > 0
    )