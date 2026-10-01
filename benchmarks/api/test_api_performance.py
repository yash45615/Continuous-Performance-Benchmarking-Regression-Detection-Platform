import requests


BASE_URL = "http://127.0.0.1:8000"


def get_health():

    response = requests.get(
        f"{BASE_URL}/health",
        timeout=5
    )

    response.raise_for_status()

    return response


def test_health_performance(benchmark):

    result = benchmark(get_health)

    assert result.status_code == 200