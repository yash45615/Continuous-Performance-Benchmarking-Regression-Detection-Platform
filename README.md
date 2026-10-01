# Continuous Performance Benchmarking & Regression Detection Platform

A performance engineering platform for building **repeatable benchmarks, establishing performance baselines, detecting regressions, profiling bottlenecks, analyzing database query performance, and generating actionable performance reports**.

The platform is designed around a continuous performance workflow:

**Workload → Benchmark → Measurement → Baseline → Variance Analysis → Regression Detection → Profiling → Triage → Report → CI Performance Gate**

---

## 🚀 Overview

Traditional load-testing tools can tell you that an application became slower, but they do not necessarily explain:

* What changed?
* How large is the regression?
* Is the result statistically reliable?
* Is the benchmark environment comparable?
* Is the bottleneck in the API, application code, or database?
* Which team should investigate it?
* Should CI block the change?

This project addresses those problems by combining:

* Controlled benchmark workloads
* Repeatable benchmark execution
* Warm-up periods
* Latency percentile measurement
* Throughput measurement
* Error-rate tracking
* Variance and noise analysis
* Baseline management
* Automated regression detection
* Application profiling
* PostgreSQL query analysis
* Regression triage
* Owner routing
* HTML/JSON performance reports
* Locust load testing
* Prometheus-compatible metrics
* CI performance gates

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │   Product / API      │
                         │      Service         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Workload Engine    │
                         │ API / DB / E2E        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Benchmark Runner   │
                         │ Warmup + Concurrency │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │      Metrics Collection      │
                    │ p50 / p95 / p99 / RPS / ERR │
                    └──────────────┬───────────────┘
                                   │
                     ┌─────────────┴─────────────┐
                     ▼                           ▼
             ┌────────────────┐         ┌────────────────┐
             │ Baseline Store │         │ Result Store   │
             └───────┬────────┘         └───────┬────────┘
                     │                          │
                     └────────────┬─────────────┘
                                  ▼
                     ┌────────────────────────┐
                     │ Regression Detection   │
                     │ Threshold + Variance   │
                     └────────────┬───────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │ Profiling & DB Analysis│
                     │ cProfile / EXPLAIN     │
                     └────────────┬───────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │ Regression Triage      │
                     │ Component + Owner      │
                     └────────────┬───────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │ HTML / JSON Reports    │
                     └────────────┬───────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │ CI Performance Gate    │
                     └────────────────────────┘
```

---

## ✨ Key Features

### 1. Repeatable Benchmarking

Benchmarks use controlled workloads and configurable parameters including:

* Number of iterations
* Warm-up iterations
* Concurrency
* Target endpoint
* Workload type
* Regression threshold

This makes benchmark runs easier to reproduce and compare.

---

### 2. Performance Metrics

The benchmark runner collects:

| Metric             | Purpose                     |
| ------------------ | --------------------------- |
| Mean latency       | Average request latency     |
| P50                | Typical request latency     |
| P95                | Tail latency                |
| P99                | High tail latency           |
| Min                | Fastest request             |
| Max                | Slowest request             |
| Standard deviation | Measurement variability     |
| RPS                | Throughput                  |
| Error rate         | Reliability under workload  |
| CPU usage          | System resource usage       |
| Memory usage       | Process/system memory usage |

---

### 3. Warm-Up and Variance Control

The platform performs warm-up requests before collecting benchmark measurements.

This helps reduce noise caused by:

* Cold application state
* Database connection initialization
* Cache initialization
* Python/runtime startup effects
* First-request overhead

Benchmark results also capture variability so noisy runs can be identified rather than automatically treated as regressions.

---

### 4. Baseline Management

A known-good benchmark result can be stored as a baseline.

Example:

```text
Benchmark: api_health

Baseline
--------
P50: 12.4 ms
P95: 19.8 ms
P99: 25.1 ms
RPS: 412.7
```

Future benchmark runs can be compared against this baseline.

---

### 5. Automated Regression Detection

The regression engine compares current results against historical baselines.

It evaluates changes in metrics such as:

```text
Latency increase
Throughput decrease
Error-rate increase
Measurement variability
```

Example:

```text
Baseline P95 : 20.0 ms
Current P95  : 24.8 ms

Change       : +24%

Threshold    : 10%

Result       : REGRESSION DETECTED
```

This can be used as a performance quality gate in CI.

---

### 6. Application Profiling

The platform includes Python profiling using:

```text
cProfile
pstats
```

This allows expensive functions and execution paths to be investigated after a performance regression is detected.

Example profiling information:

```text
ncalls
tottime
percall
cumtime
function
```

---

### 7. PostgreSQL Performance Analysis

Database workloads can be analyzed using PostgreSQL execution plans.

The project supports analysis using:

```sql
EXPLAIN (ANALYZE, BUFFERS)
```

This helps investigate:

* Sequential scans
* Index scans
* Join strategies
* Row estimates
* Buffer usage
* Planning time
* Execution time

The goal is to connect an observed API regression with the underlying database behavior.

---

### 8. Regression Triage

Instead of stopping at:

```text
Performance regression detected
```

the platform provides a triage workflow that can identify the likely affected component and route the issue toward an appropriate owner.

Example:

```text
Benchmark
    ↓
Latency Regression
    ↓
Database Investigation
    ↓
Query Plan Comparison
    ↓
Database Owner
```

---

### 9. Performance Reports

Benchmark results can be converted into structured reports containing:

* Benchmark information
* Baseline measurements
* Current measurements
* Metric deltas
* Regression status
* Environment information
* Resource utilization
* Triage information

Reports are available in machine-readable JSON and human-readable HTML formats.

---

### 10. Load Testing with Locust

The platform also includes Locust workloads for more realistic traffic patterns.

Supported scenarios can include:

* Read-heavy workloads
* Search workloads
* Mixed workloads
* Write workloads

Run:

```powershell
locust -f load_tests/locustfile.py
```

Then open:

```text
http://localhost:8089
```

---

### 11. Prometheus-Compatible Metrics

The API exposes performance metrics through:

```text
/metrics
```

This makes the application suitable for integration with monitoring systems such as Prometheus and visualization platforms such as Grafana.

---

### 12. CI/CD Performance Gates

Performance checks can be integrated into GitHub Actions.

The intended workflow is:

```text
Pull Request
     ↓
Build
     ↓
Run Tests
     ↓
Run Benchmark
     ↓
Compare Baseline
     ↓
Detect Regression
     ↓
Performance Gate
     ↓
Pass / Fail
```

This allows performance to become part of the engineering feedback loop rather than a separate manual testing activity.

---

# 📁 Project Structure

```text
continuous-performance-platform/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   │
│   └── tests/
│
├── benchmarks/
│   ├── api/
│   ├── database/
│   ├── workloads/
│   ├── benchmark_config.yml
│   ├── environment.py
│   ├── reproducibility.yml
│   ├── result.py
│   ├── runner.py
│   └── warmup.py
│
├── load_tests/
│   └── locustfile.py
│
├── profiling/
│   ├── profile_api.py
│   ├── profile_database.py
│   └── reports/
│
├── regression/
│   ├── baseline.py
│   ├── comparator.py
│   └── detector.py
│
├── triage/
│   ├── analyzer.py
│   ├── router.py
│   └── owners.yaml
│
├── reports/
│   ├── generator.py
│   └── templates/
│
├── scripts/
│   ├── check_regression.py
│   ├── generate_report.py
│   ├── performance_gate.py
│   ├── run_benchmark.py
│   ├── run_full_benchmark.py
│   ├── run_repeated_benchmark.py
│   ├── seed_database.py
│   └── trend_analysis.py
│
├── data/
│   ├── baselines/
│   └── results/
│
├── tests/
│
├── .github/
│   └── workflows/
│       └── performance.yml
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🛠️ Technology Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL

### Performance Engineering

* Locust
* pytest-benchmark
* asyncio/httpx
* NumPy
* Pandas
* psutil

### Profiling

* cProfile
* pstats
* PostgreSQL `EXPLAIN ANALYZE`

### Observability

* Prometheus client
* JSON metrics
* HTML reports

### Testing

* Pytest
* pytest-benchmark

### CI/CD

* GitHub Actions

---

# 💻 Local Setup

## Prerequisites

Install:

* Python 3.10+
* PostgreSQL
* Git

Docker is **not required** for local development.

---

## 1. Clone the repository

```powershell
git clone https://github.com/YOUR_USERNAME/continuous-performance-benchmarking-platform.git
cd continuous-performance-benchmarking-platform
```

---

## 2. Create virtual environment

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Configure environment

Create a `.env` file:

```text
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/performance_benchmark_db
BASE_URL=http://127.0.0.1:8000
REGRESSION_THRESHOLD_PERCENT=10
```

Do not commit `.env`.

---

# ▶️ Run the API

```powershell
uvicorn backend.app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

# 🗄️ Seed the Database

Run:

```powershell
python scripts/seed_database.py
```

Verify the database contains benchmark data and application records.

---

# ⚡ Run a Benchmark

```powershell
python scripts/run_benchmark.py
```

Benchmark results are stored under:

```text
data/results/
```

Example metrics:

```text
Mean
P50
P95
P99
RPS
Error Rate
Standard Deviation
CPU
Memory
```

---

# 🔁 Run Repeated Benchmarks

For additional variance analysis:

```powershell
python scripts/run_repeated_benchmark.py
```

This allows multiple runs to be compared rather than relying on a single measurement.

---

# 🚨 Run Regression Detection

Use:

```powershell
python scripts/check_regression.py
```

The script compares the current benchmark against the stored baseline and reports whether the configured performance threshold has been exceeded.

---

# 📊 Generate Performance Report

```powershell
python scripts/generate_report.py
```

Reports are generated under the project's report/result directories.

---

# 🔬 Run Profiling

API profiling:

```powershell
python profiling/profile_api.py
```

Database profiling can be performed using PostgreSQL execution plans:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT ...;
```

---

# 🧪 Run Tests

```powershell
pytest
```

For benchmark-related tests:

```powershell
pytest --benchmark-only
```

---

# 🚦 Performance Gate

Run:

```powershell
python scripts/performance_gate.py
```

The performance gate can be used by CI to determine whether a benchmark change exceeds the configured threshold.

---

# 🌐 Run Locust

```powershell
locust -f load_tests/locustfile.py
```

Open:

```text
http://localhost:8089
```

Configure the number of users and spawn rate, then start the test.

---

# 📈 Benchmark Methodology

The platform follows a controlled measurement methodology.

### Step 1 — Define workload

Specify:

* Endpoint
* Request type
* Dataset
* Iterations
* Concurrency

### Step 2 — Warm up

Execute warm-up requests before measurement.

### Step 3 — Measure

Collect:

* Latency
* Throughput
* Errors
* CPU
* Memory

### Step 4 — Calculate statistics

Calculate:

```text
Mean
P50
P95
P99
Standard deviation
RPS
Error rate
```

### Step 5 — Store baseline

Save an accepted performance result.

### Step 6 — Compare future runs

Calculate metric deltas against the baseline.

### Step 7 — Check variance

Identify whether the result is sufficiently stable for comparison.

### Step 8 — Detect regression

Apply configured thresholds.

### Step 9 — Investigate

Use:

```text
cProfile
PostgreSQL EXPLAIN ANALYZE
Query-plan comparison
```

### Step 10 — Triage

Identify the likely component and owner.

### Step 11 — Generate report

Produce JSON and HTML results.

### Step 12 — Apply CI gate

Allow or block the change based on configured performance criteria.

---

# 📌 Example Performance Workflow

```text
Developer changes database query
            ↓
Pull Request
            ↓
Benchmark executes
            ↓
P95 increases
            ↓
Baseline comparison
            ↓
Regression detected
            ↓
Query plan analyzed
            ↓
Index / query behavior investigated
            ↓
Triage routes issue
            ↓
Performance report generated
            ↓
CI performance gate
```

---

# 🎯 Engineering Goals

This project focuses on the engineering problems behind reliable performance measurement:

* Reproducibility
* Controlled variance
* Benchmark methodology
* Baseline management
* Regression detection
* Tail-latency analysis
* Throughput measurement
* Database performance analysis
* Profiling
* Root-cause investigation
* Automated triage
* Performance reporting
* CI/CD integration
* Self-service performance testing

---

# 📸 Project Screenshots

Add project evidence here after uploading screenshots to the repository.

Recommended screenshots:

### FastAPI Benchmark API

```text
docs/screenshots/01-fastapi-swagger.png
```

### Benchmark Execution

```text
docs/screenshots/04-benchmark-run.png
```

### Regression Detection

```text
docs/screenshots/07-regression-detection.png
```

### cProfile

```text
docs/screenshots/08-cprofile.png
```

### PostgreSQL EXPLAIN ANALYZE

```text
docs/screenshots/09-postgresql-explain.png
```

### Performance Report

```text
docs/screenshots/11-performance-report.png
```

### Locust

```text
docs/screenshots/12-locust-load-test.png
```

---

# 🔐 Security

The repository intentionally excludes:

```text
.env
database passwords
API keys
virtual environments
generated profiling files
temporary logs
```

Use environment variables for local credentials and secrets.

---

# 🚧 Future Enhancements

Potential extensions include:

* Distributed benchmark execution
* Cloud-based benchmark workers
* Grafana dashboards
* Prometheus time-series storage
* Automated flamegraph generation
* GitHub PR performance comments
* Historical performance trends
* Query-level regression attribution
* Kubernetes benchmark environments
* Multi-region benchmarking
* Hardware/environment normalization
* Statistical significance testing
* Automated benchmark workload generation

---

# 👨‍💻 Author

**Yash**

Performance Engineering | SDET | Backend | Test Automation

---

# ⭐ Project Focus

This project demonstrates an end-to-end approach to **continuous performance engineering**, moving beyond basic load testing toward:

```text
Measure
  ↓
Baseline
  ↓
Control Variance
  ↓
Detect
  ↓
Profile
  ↓
Investigate
  ↓
Triage
  ↓
Report
  ↓
Gate
```

The objective is to make performance measurements **repeatable, explainable, actionable, and continuously enforceable**.
