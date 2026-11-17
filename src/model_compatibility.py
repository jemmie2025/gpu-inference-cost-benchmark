import csv
import json
from pathlib import Path

from src.model_sizing import estimate_memory, check_memory_fit


def main():
    models = sorted(Path("configs/models").glob("*.json"))

    profiles = json.loads(
        Path("configs/providers/gpu-profiles.json").read_text()
    )["gpus"]

    results = []

    for path in models:
        model = json.loads(path.read_text())

        memory = estimate_memory(
            model["parameters_billions"],
            model["weight_precision_bits"],
            model["tensor_parallel_size"]
        )

        for gpu in profiles:
            available = gpu["vram_gb"]
            required = memory["estimated_per_gpu_gib"]

            fits = check_memory_fit(
                required,
                available,
                model["gpu_memory_utilization"]
            )

            results.append({
                "model": model["model_id"],
                "parameters_billions": model["parameters_billions"],
                "precision_bits": model["weight_precision_bits"],
                "quantization": model["quantization"] or "none",
                "gpu": gpu["name"],
                "nominal_vram_gib": available,
                "required_gpu_count": memory["required_gpu_count"],
                "weight_memory_gib": memory["weight_memory_gib"],
                "estimated_per_gpu_gib": required,
                "memory_fit": "pass" if fits else "fail",
                "measurement_type": "estimated",
                "runtime_validation": "pending"
            })

    output = Path("results/model-compatibility.csv")
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=results[0].keys(),
            lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"PASS: Generated {len(results)} model-GPU assessments")
    print(f"Report: {output}")


if __name__ == "__main__":
    main()
