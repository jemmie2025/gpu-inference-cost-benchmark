# GPU Cost Comparison

## Dedicated GPU Economics

Modeled workload: 100 output tokens/sec, 50% utilization, excluding additional overhead.

| Provider | GPU | Billing | Price captured | USD/hour | USD/M tokens | Monthly USD |
|---|---|---|---|---:|---:|---:|
| GCP | L4 | spot | 2026-11-17 | 0.60 | 3.33 | 437.01 |
| RunPod | L4 | on-demand | 2026-11-17 | 0.69 | 3.83 | 503.70 |
| GCP | L4 | on-demand | 2026-11-17 | 1.00 | 5.56 | 730.30 |
| RunPod | L40S | on-demand | 2026-11-17 | 1.09 | 6.06 | 795.70 |
| Lambda | A100 | on-demand | 2026-11-17 | 1.99 | 11.06 | 1452.70 |
| Lambda | H100 | on-demand | 2026-11-17 | 3.79 | 21.06 | 2766.70 |

## Utilization Analysis

![Utilization Analysis](utilization-analysis.png)

## Limitations

- Throughput values are modeled assumptions.
- Unverified prices are excluded from rankings.
- Serverless economics are reported separately.
- Live GPU performance remains unverified.
