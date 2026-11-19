import csv
from pathlib import Path

from src.cost_engine import calculate_cost


def main():
    with open("results/model-compatibility.csv") as f:
        models = list(csv.DictReader(f))

    with open("configs/providers/pricing.csv") as f:
        providers = list(csv.DictReader(f))

    results = []

    for model in models:
        if model["memory_fit"] != "pass":
            continue

        for provider in providers:
            if provider["billing"] == "serverless":
                continue

            if provider["price_status"] != "published":
                continue

            if provider["cost_scope"] != "instance":
                continue

            gpu = model["gpu"].replace("NVIDIA ", "")

            if provider["gpu"] != gpu:
                continue

            required = int(model["required_gpu_count"])
            available = int(provider["gpu_count"])

            if available != required:
                continue

            rate = float(provider["usd_per_hour"])

            for throughput in [50, 100, 200]:
                for utilization in [0.25, 0.50, 0.75, 1.0]:

                    metrics = calculate_cost(
                        rate, throughput, utilization
                    )

                    results.append({
                        "model": model["model"],
                        "precision_bits": model["precision_bits"],
                        "quantization": model["quantization"],
                        "provider": provider["provider"],
                        "price_captured_at": provider["price_captured_at"],
                        "price_source_url": provider["price_source_url"],
                        "price_status": provider["price_status"],
                        "gpu": gpu,
                        "gpu_count": required,
                        "billing": provider["billing"],
                        "assumed_throughput": throughput,
                        "utilization": utilization,
                        "measurement_type": "modeled",
                        **metrics
                    })

    if not results:
        raise RuntimeError("No eligible model-provider scenarios")

    output = Path("results/model-cost-comparison.csv")

    with output.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=results[0].keys(),
            lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"PASS: Generated {len(results)} model-cost scenarios")
    print(f"Report: {output}")


if __name__ == "__main__":
    main()
