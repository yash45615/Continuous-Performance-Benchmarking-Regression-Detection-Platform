from locust import (
    HttpUser,
    between,
    task
)


class PerformanceUser(HttpUser):

    wait_time = between(
        0.2,
        1.0
    )

    @task(40)
    def product_list(self):

        self.client.get(
            "/products/?limit=50",
            name="GET /products"
        )

    @task(25)
    def product_detail(self):

        self.client.get(
            "/products/50000",
            name="GET /products/{id}"
        )

    @task(20)
    def product_search(self):

        self.client.get(
            "/products/search?q=Laptop",
            name="GET /products/search"
        )

    @task(10)
    def product_summary(self):

        self.client.get(
            "/products/summary",
            name="GET /products/summary"
        )

    @task(5)
    def health(self):

        self.client.get(
            "/health",
            name="GET /health"
        )