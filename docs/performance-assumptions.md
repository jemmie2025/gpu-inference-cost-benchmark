# Performance Assumptions

## Throughput

| Scenario | Output tokens/sec | Source |
|---|---:|---|
| Low | 50 | Synthetic assumption |
| Reference | 100 | Synthetic assumption |
| High | 200 | Synthetic assumption |

These values are author-defined sensitivity inputs.
They are not derived from vendor performance tables,
vLLM benchmarks or empirical GPU measurements.

The same scenarios are applied across eligible
model-GPU combinations for controlled cost comparison.
They do not represent hardware-specific predictions.

## Latency

TTFT, inter-token latency and P95 latency remain
unmeasured. No latency targets or results are fabricated.

## Uncertainty

Cost per million output tokens depends on hourly pricing,
assumed throughput and workload utilization.

Uncertainty in both pricing and throughput propagates
into the final cost estimates. Results are conditional
scenarios, not validated production cost forecasts.

## Future Validation

Run the reference inference workload on each eligible
model-GPU configuration and replace synthetic throughput
inputs with timestamped empirical measurements.
