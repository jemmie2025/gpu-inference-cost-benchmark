import math


def estimate_memory(parameters_billions, precision_bits,
                    tensor_parallel_size=1,
                    overhead_ratio=0.20,
                    runtime_reserve_gib=4.0):

    if not math.isfinite(parameters_billions):
        raise ValueError("Invalid parameter count")

    if parameters_billions <= 0:
        raise ValueError("Parameter count must be positive")

    if precision_bits not in (4, 8, 16, 32):
        raise ValueError("Unsupported precision")

    if tensor_parallel_size not in (1, 2, 4, 8):
        raise ValueError("Unsupported tensor parallel size")

    if not all(math.isfinite(v) and v >= 0 for v in
               (overhead_ratio, runtime_reserve_gib)):
        raise ValueError("Invalid memory overhead")

    weight_gib = (
        parameters_billions * 1e9 * precision_bits
        / 8 / (1024 ** 3)
    )

    per_gpu = (
        weight_gib * (1 + overhead_ratio)
        / tensor_parallel_size
        + runtime_reserve_gib
    )

    return {
        "weight_memory_gib": round(weight_gib, 3),
        "estimated_per_gpu_gib": round(per_gpu, 3),
        "required_gpu_count": tensor_parallel_size,
        "measurement_type": "estimated"
    }


def check_memory_fit(required_gib, available_gib,
                     utilization=0.90):

    if not 0 < utilization <= 1:
        raise ValueError("Invalid memory utilization")

    return required_gib <= available_gib * utilization
