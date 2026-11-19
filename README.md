# GPU Inference Cost Model

[![CI](https://github.com/jemmie2025/gpu-inference-cost-model/actions/workflows/ci.yml/badge.svg)](https://github.com/jemmie2025/gpu-inference-cost-model/actions/workflows/ci.yml)

## Overview

Multi-cloud GPU inference cost modeling and FinOps
framework for evaluating LLM serving performance,
GPU capacity, token economics, and deployment efficiency.

## Provider Coverage

AWS, Google Cloud, Lambda Labs, RunPod, Modal, and Replicate.

## Model Portfolio

| Model | Precision | GPU Count |
|---|---|---:|
| Qwen3-0.6B | BF16 | 1 |
| Qwen2.5-7B-Instruct | BF16 | 1 |
| Llama-3.1-8B-Instruct | AWQ INT4 | 1 |
| Qwen2.5-32B-Instruct | AWQ INT4 | 1 |
| Llama-3.3-70B-Instruct | BF16 | 4 |

## Reference Workload

| Component | Configuration |
|---|---|
| Inference Engine | vLLM |
| Context Limit | 4096 tokens |
| Target Input / Output | 512 / 256 tokens |
| Concurrency | 1, 8, 32 |
| GPU Utilization Scenarios | 25–100% |
| Infrastructure Overhead | 0–20% |
| Cold-start Scenarios | 0–30 seconds |

## Technical Stack

Python, Docker, Kubernetes, NVIDIA CUDA, vLLM,
Pytest, Matplotlib, and GitHub Actions.

## Architecture

Configuration → Pricing and Assumptions → Cost Analysis →
Automated Validation → Deployment Recommendations

## Capabilities

- Multi-cloud pricing and billing comparison.
- Cost per million output tokens.
- Concurrent inference and streaming latency analysis.
- GPU telemetry and memory capacity estimation.
- Quantization and tensor parallelism assessment.
- Utilization and serverless cold-start sensitivity.
- Automated testing and CI validation.

## Validation Summary

| Metric | Result |
|---|---:|
| Cloud Providers | 6 |
| Pricing Configurations | 12 |
| LLM Configurations | 5 |
| GPU Profiles | 5 |
| Dedicated Cost Scenarios | 288 |
| Serverless Cost Scenarios | 144 |
| Model Cost Scenarios | 252 |
| Total Modeled Cost Scenarios | 684 |
| Model-GPU Assessments | 25 |
| Utilization Scenarios | 24 |
| Automated Tests | 30 passed |

## Cost Analysis

![GPU Cost Analysis](results/utilization-analysis.png)

## Results

- [Provider Comparison](results/provider-comparison.md)
- [Dedicated GPU Costs](results/cost-comparison.csv)
- [Serverless Costs](results/serverless-comparison.csv)
- [Utilization Analysis](results/utilization-sensitivity.csv)
- [GPU Compatibility](results/model-compatibility.csv)
- [Model Cost Comparison](results/model-cost-comparison.csv)

## Reproduce

Run `make install` followed by `make check`.

## Documentation

- [Architecture](docs/architecture.md)
- [Methodology](docs/methodology.md)
- [Pricing Sources](docs/pricing-sources.md)
- [Model Deployment](docs/model-deployment.md)
- [Decision Guide](docs/decision-guide.md)

## Validation Evidence

### Automated Validation

![Automated Validation](evidence/screenshots/01-automated-validation.png)

### Provider Cost Comparison

![Provider Comparison](evidence/screenshots/02-provider-cost-comparison.png)

## Limitations

Cost scenarios and GPU memory assessments are modeled.
Live GPU performance, runtime compatibility, and
official AWS regional pricing confirmation remain pending.
