# Benchmark Methodology

## Goals

The benchmark system measures:

- latency
- throughput
- error rate
- CPU usage
- memory usage
- variance
- database execution behavior

## Measurement process

1. Start the application.
2. Verify application health.
3. Warm up the workload.
4. Execute multiple measurement runs.
5. Record P50, P95 and P99.
6. Record throughput.
7. Record errors.
8. Capture environment metadata.
9. Compare against baseline.
10. Generate regression report.
11. Profile database queries when required.
12. Route regressions for triage.

## Variance control

The platform controls measurement variance through:

- fixed dataset
- fixed concurrency
- warm-up requests
- repeated measurements
- environment fingerprinting
- percentile-based reporting
- standard deviation
- coefficient of variation

## Regression policy

Default thresholds:

- latency increase > 10% = regression
- throughput decrease > 10% = regression

These thresholds are configurable.

## Database methodology

Database performance is analyzed using:

EXPLAIN ANALYZE

with:

- execution time
- estimated cost
- actual rows
- scan type
- buffer information

## Reproducibility

Each result records environment information so that measurements can be reproduced under equivalent conditions.