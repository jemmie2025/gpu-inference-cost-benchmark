import csv
import json
from pathlib import Path


def main():
    config = json.loads(
        Path("configs/workloads/performance-assumptions.json").read_text()
    )

    throughput = config["throughput"]

    with open("results/model-compatibility.csv") as f:
        combinations = list(csv.DictReader(f))

    rows = []

    for item in combinations:
        for scenario, value in throughput["scenarios"].items():
            rows.append({
                "model": item["model"],
                "gpu": item["gpu"],
                "gpu_count": item["required_gpu_count"],
                "memory_fit": item["memory_fit"],
                "scenario": scenario,
                "assumed_output_tokens_per_second": value,
                "throughput_source": throughput["source"],
                "confidence": throughput["confidence"],
                "hardware_calibrated": False,
                "latency_status": "unmeasured",
                "runtime_validation": "pending"
            })

    output = Path("results/performance-assumptions.csv")

    with output.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=rows[0].keys(),
            lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"PASS: Generated {len(rows)} assumption records")


if __name__ == "__main__":
    main()
