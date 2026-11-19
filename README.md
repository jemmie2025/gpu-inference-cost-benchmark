# GPU Inference Cost Model

[![CI](https://github.com/jemmie2025/gpu-inference-cost-model/actions/workflows/ci.yml/badge.svg)](https://github.com/jemmie2025/gpu-inference-cost-model/actions/workflows/ci.yml)

## Overview

A reproducible multi-cloud GPU inference cost model for
evaluating token economics, GPU memory requirements,
and infrastructure pricing across AWS, GCP, Lambda,
RunPod, Modal, and Replicate.

## Architecture

Pricing Sources + Performance Assumptions
→ GPU Capacity Screening → Cost Modeling
→ Sensitivity Analysis → Reports

## Model Portfolio

| Model | Precision | Configured GPUs |
|---|---|---:|
| Qwen3-0.6B | BF16 | 1 |
| Qwen2.5-7B | BF16 | 1 |
| Llama-3.1-8B | AWQ INT4 | 1 |
| Qwen2.5-32B | AWQ INT4 | 1 |
| Llama-3.3-70B | BF16 | 4 |

GPU memory fit is estimated, not runtime-verified.

## Pricing and Performance Assumptions

| Parameter | Assumption |
|---|---|
| Pricing snapshot | 2026-11-17 |
| Currency | USD |
| Output throughput | 50, 100, 200 tokens/sec |
| Throughput source | Author-defined synthetic scenarios |
| Utilization | 25–100% |
| Infrastructure overhead | 0–20% |
| Cold-start duration | 0–30 seconds |
| Empirical latency | Unmeasured |

Throughput assumptions are not hardware-calibrated.
Cost estimates are conditional on pricing and assumed
performance, with uncertainty in both inputs.

AWS secondary-source prices remain provisional.

## Coverage

| Metric | Count |
|---|---:|
| Cloud providers | 6 |
| Pricing configurations | 12 |
| LLM configurations | 5 |
| GPU profiles | 5 |
| Dedicated cost scenarios | 288 |
| Serverless cost scenarios | 144 |
| Model-specific cost scenarios | 252 |
| Total modeled cost scenarios | 684 |
| GPU memory assessments | 25 |
| Performance assumption records | 75 |

## Code Validation

41 automated tests passing locally.

Tests validate cost calculations, input handling,
simulated HTTP integration, and metadata traceability.
They do not establish empirical GPU performance or
confirm the accuracy of market pricing.

## Cost Sensitivity

![Modeled GPU Cost Sensitivity](results/utilization-analysis.png)

## Reports

| Report | Output |
|---|---|
| Provider comparison | [Markdown](results/provider-comparison.md) |
| Dedicated costs | [CSV](results/cost-comparison.csv) |
| Serverless costs | [CSV](results/serverless-comparison.csv) |
| Utilization sensitivity | [CSV](results/utilization-sensitivity.csv) |
| GPU memory assessments | [CSV](results/model-compatibility.csv) |
| Model-specific costs | [CSV](results/model-cost-comparison.csv) |
| Performance assumptions | [CSV](results/performance-assumptions.csv) |

## Infrastructure

Docker Compose and Kubernetes configurations are
defined and statically checked but not executed
on GPU hardware.

See [Reference Deployment](infrastructure/README.md).

## Reproduce

Run `make install` followed by `make check`.

Report regeneration uses the stored pricing snapshot
and does not retrieve current market prices.

## Documentation

[Architecture](docs/architecture.md) |
[Methodology](docs/methodology.md) |
[Pricing Sources](docs/pricing-sources.md) |
[Performance Assumptions](docs/performance-assumptions.md) |
[Model Deployment](docs/model-deployment.md) |
[Decision Guide](docs/decision-guide.md)

## Limitations

No empirical GPU inference runs were performed.
Throughput, memory fit, and token costs are modeled.
Production decisions require refreshed pricing,
hardware-specific measurements, and runtime validation.
