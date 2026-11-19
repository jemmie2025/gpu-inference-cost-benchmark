# Reference Deployment Configurations

## Status

Defined and statically checked, but not executed on GPU hardware.

These configurations support future empirical validation
of the throughput assumptions used by the cost model.

| Component | Purpose | Status |
|---|---|---|
| Docker Compose | Local vLLM GPU serving | Configuration checked |
| Kubernetes | GPU-enabled inference deployment | YAML parsed |

## Runtime Prerequisites

- Compatible NVIDIA GPU and drivers.
- NVIDIA Container Toolkit.
- GPU-enabled Kubernetes nodes and device plugin.
- Verified vLLM image and model revisions.
- Sufficient GPU memory and persistent storage.

No GPU deployment, live latency measurement or
inference throughput measurement was performed.

These configurations are reference implementations,
not production-validated infrastructure.
