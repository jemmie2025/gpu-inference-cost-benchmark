# Benchmark Methodology

## Workload

- Model: Qwen2.5-7B-Instruct
- Engine: vLLM
- Precision: BF16
- Target input/output: 512/256 tokens
- Concurrency: 1, 8, 32
- Warm-up requests: 10 per concurrency
- Requests per run: 100
- Repetitions: 3

## Cost Model

Dedicated infrastructure:

Cost/M tokens = Hourly cost × 1,000,000 /
(Throughput × Utilization × 3600)

Serverless infrastructure:

Cost/M tokens = Request cost × 1,000,000 /
Generated tokens

## Sensitivity Analysis

- Throughput: 50, 100, 200 tokens/sec
- Utilization: 25%, 50%, 75%, 100%
- Infrastructure overhead: 0%, 10%, 20%
- Cold starts: 0, 5, 15, 30 seconds

## Validation

- 21 automated tests.
- 216 dedicated GPU cost scenarios.
- 108 serverless cost scenarios.
- 16 utilization sensitivity scenarios.
- Docker and Kubernetes configuration checks.

## Limitations

- Throughput assumptions are modeled, not measured.
- Exact input token length is not yet enforced.
- Live GPU execution requires compatible hardware.
- GPU telemetry is sampled rather than continuous.
- Streaming latency is measured at chunk level.
- Pending prices and additional billing costs
  require provider-specific verification.
