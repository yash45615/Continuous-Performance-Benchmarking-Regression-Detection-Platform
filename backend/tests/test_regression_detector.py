from regression.detector import detect_regression


def test_no_regression():

    result = detect_regression(
        benchmark_name="api_health",
        baseline=100,
        current=105,
        threshold_percent=10
    )

    assert result.regression is False


def test_regression():

    result = detect_regression(
        benchmark_name="api_health",
        baseline=100,
        current=120,
        threshold_percent=10
    )

    assert result.regression is True


def test_negative_change():

    result = detect_regression(
        benchmark_name="api_health",
        baseline=100,
        current=80,
        threshold_percent=10
    )

    assert result.regression is False