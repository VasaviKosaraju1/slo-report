# Validation

Local verification on Python 3.9.6 using synthetic inputs.

## Tests

```text
test_4xx_is_not_server_failure (test_slo.Tests) ... ok
test_boundary_budget (test_slo.Tests) ... ok
test_duplicate_request (test_slo.Tests) ... ok
test_empty_window (test_slo.Tests) ... ok
test_invalid_target (test_slo.Tests) ... ok
test_no_mutation (test_slo.Tests) ... ok
test_nonfinite_latency (test_slo.Tests) ... ok
test_percentile_nearest_rank (test_slo.Tests) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.000s

OK
```

## Example

```sh
python3 slo.py sample.json
```

Exit status: 1. A nonzero policy result is expected for the failing example and is not a test failure.

```text
{
  "requests": 10,
  "failed_requests": 1,
  "availability": 0.9,
  "availability_target": 0.99,
  "allowed_failed_requests": 0.1,
  "error_budget_remaining_requests": -0.9,
  "error_budget_consumed_ratio": 9.999999999999991,
  "availability_met": false,
  "latency_threshold_ms": 200,
  "requests_within_latency_ratio": 0.8,
  "p50_latency_ms": 130,
  "p95_latency_ms": 230
}
```

These results demonstrate the included fixtures. They do not establish production readiness or performance on real customer data.
