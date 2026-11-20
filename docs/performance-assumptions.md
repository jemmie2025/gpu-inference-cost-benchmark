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

## Infrastructure Cost Overhead

| Scenario | Overhead | Interpretation |
|---|---:|---|
| Baseline | 0% | Base compute price only |
| Moderate | 10% | Illustrative additional expenses |
| Stress | 20% | Higher additional cost exposure |

Source: Author-defined sensitivity assumptions.

Supporting reference:
[AWS EC2 Pricing Calculator](https://docs.aws.amazon.com/pricing-calculator/latest/userguide/ec2-estimates.html)

AWS documents additional storage, monitoring and networking
costs. The selected percentages are not AWS-published rates
or empirically measured provider overheads.

Actual overhead may exceed 20%.

## Serverless Cold Starts

| Scenario | Duration |
|---|---:|
| Warm | 0 seconds |
| Short | 5 seconds |
| Moderate | 15 seconds |
| Stress | 30 seconds |

Source: Author-defined sensitivity assumptions.

Supporting reference:
[Modal LLM Initialization and Latency](https://modal.com/docs/examples/trtllm_latency)

Cold starts depend on container initialization, model loading,
weight caching and infrastructure availability.

The selected durations are illustrative scenarios, not measured
provider latency or guaranteed upper bounds.

The serverless model assumes initialization and idle time are
billable. Actual billing policies require provider-specific
verification.

## Assumption Traceability

Overhead and cold-start inputs are defined in
configs/workloads/performance-assumptions.json.

Generated dedicated and serverless cost reports include
the corresponding assumption sources and reference URLs.

Documentation does not constitute empirical calibration.
