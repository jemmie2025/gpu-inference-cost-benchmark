# Model Deployment and GPU Capacity

## Model Portfolio

| Model | Precision | GPU Count |
|---|---|---:|
| Qwen3-0.6B | BF16 | 1 |
| Qwen2.5-7B | BF16 | 1 |
| Llama-3.1-8B | AWQ INT4 | 1 |
| Qwen2.5-32B | AWQ INT4 | 1 |
| Llama-3.3-70B | BF16 | 4 |

## Capacity Planning

GPU memory estimates account for model weights,
quantization, tensor parallelism, runtime overhead
and memory utilization limits.

## Deployment Controls

- Validate GPU memory and CUDA compatibility.
- Pin model revisions and container versions.
- Verify quantization support.
- Validate multi-GPU interconnect performance.
- Monitor latency, throughput and resource utilization.

## Results

- 25 model-GPU memory assessments.
- 252 model-specific cost scenarios.
- 41 passing automated tests.

## Limitations

Memory requirements and costs are modeled estimates.
Live GPU performance remains unverified.
The 70B model requires a verified multi-GPU deployment
and is excluded from single-GPU cost comparisons.
