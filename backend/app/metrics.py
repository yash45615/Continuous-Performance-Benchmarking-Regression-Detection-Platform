from prometheus_client import Counter, Histogram


REQUEST_COUNT = Counter(
    "performance_platform_requests_total",
    "Total HTTP requests"
)


REQUEST_LATENCY = Histogram(
    "performance_platform_request_latency_seconds",
    "HTTP request latency"
)


ERROR_COUNT = Counter(
    "performance_platform_errors_total",
    "Total HTTP errors"
)