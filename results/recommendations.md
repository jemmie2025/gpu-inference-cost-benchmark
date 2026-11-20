# Workload-Specific Recommendations

Dedicated reference: 100 assumed output tokens/sec,
75% utilization and zero additional cost overhead.

Serverless reference: 256 output tokens, 100 assumed
tokens/sec, five-second cold start and zero idle time.

| Use case | Provider | Model | GPU | USD/M tokens | Status |
|---|---|---|---|---:|---|
| Lightweight classification and routing | GCP | Qwen/Qwen3-0.6B | L4 | 3.71 | US-regional modeled winner |
| Continuous general-purpose inference | RunPod | Qwen/Qwen3-8B | L40S | 4.04 | Indicative; regional quote required |
| Lightweight interruption-tolerant batch inference | GCP | Qwen/Qwen3-0.6B | L4 | 2.22 | US-regional modeled winner |
| Memory-efficient 8B inference | GCP | hugging-quants/Meta-Llama-3.1-8B-Instruct-AWQ-INT4 | L4 | 3.71 | US-regional modeled winner |
| Quantized large-model inference | RunPod | Qwen/Qwen3-32B-AWQ | L40S | 4.04 | Indicative; regional quote required |
| Intermittent serverless inference | Replicate | Qwen/Qwen3-8B | L40S | 28.79 | Indicative hardware-rate estimate; model deployment unverified |
| 70B multi-GPU inference | No eligible priced configuration | meta-llama/Llama-3.3-70B-Instruct | 4 x A100 80GB or H100 80GB | N/A | Multi-GPU quotation and runtime validation required |

## Interpretation

- Regional candidates take precedence over unconfirmed rates.
- Indicative winners are not verified US-region winners.
- Model selection reflects intended workload and estimated memory fit.
- Model quality, latency and throughput have not been benchmarked.
- Spot capacity requires interruption handling.
- Serverless estimates exclude incompatible billing scopes.
- No provider winner is declared for the 70B configuration.
- Refresh prices and measure performance before procurement.
