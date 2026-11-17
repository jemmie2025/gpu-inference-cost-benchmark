# GPU Inference Cost Benchmark

## Overview

Multi-cloud GPU inference benchmarking framework for
evaluating LLM serving performance, infrastructure costs,
and deployment efficiency.

## Provider Coverage

AWS, Google Cloud, Lambda Labs, RunPod, Modal, and Replicate.

## Model Configuration

| Component | Configuration |
|---|---|
| Primary Model | Qwen2.5-7B-Instruct |
| Secondary Model | 70B-class (optional) |
| Inference Engine | vLLM |
| Precision | BF16 / INT4 |
| Context Window | 4096 tokens |
| Input / Output | 512 / 256 tokens |
| Concurrency | 1, 8, 32 |

## Technical Stack

Python, Docker, Kubernetes, NVIDIA CUDA, vLLM,
Pytest, and GitHub Actions.

## Evaluation Metrics

- GPU hourly pricing and cost per million tokens
- Inference throughput and latency
- GPU memory and resource utilization
- Spot, on-demand, and serverless cost efficiency
- Scalability, reliability, and cold-start performance

## Architecture

Configuration → Benchmark Execution → Cost Analysis →
Automated Validation → Deployment Recommendations

## Documentation

- [Architecture](docs/architecture.md)
- [Methodology](docs/methodology.md)
- [Pricing Sources](docs/pricing-sources.md)
- [Decision Guide](docs/decision-guide.md)

## Validation

Measured results and modeled estimates are reported
separately to ensure accuracy and reproducibility.

## Status

| Validation | Result |
|---|---:|
| Automated Tests | 30 passed |
| Dedicated GPU Scenarios | 288 |
| Serverless Scenarios | 144 |
| Utilization Scenarios | 24 |
| Live GPU Benchmark | Pending |

## Reproduce

Run `make install` followed by `make check`.

## Results

- [Provider Comparison](results/provider-comparison.md)
- [Dedicated GPU Costs](results/cost-comparison.csv)
- [Serverless Costs](results/serverless-comparison.csv)
- [Utilization Analysis](results/utilization-sensitivity.csv)

![GPU Cost Analysis](results/utilization-analysis.png)


## Multi-Model Analysis

Five LLM configurations covering 0.6B to 70B parameters,
BF16 and AWQ INT4 precision, GPU memory sizing and
tensor parallelism.

| Metric | Result |
|---|---:|
| Model Configurations | 5 |
| GPU Profiles | 5 |
| Model-GPU Assessments | 25 |
| Model Cost Scenarios | 252 |
| Total Cost Scenarios | 684 |

- [Model Deployment](docs/model-deployment.md)
- [GPU Compatibility](results/model-compatibility.csv)
- [Model Cost Comparison](results/model-cost-comparison.csv)
