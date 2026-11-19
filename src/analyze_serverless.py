import json
import csv
from pathlib import Path

from src.serverless import calculate_serverless_cost


def main():
    assumptions = json.loads(
        Path("configs/workloads/performance-assumptions.json").read_text()
    )["throughput"]

    results = []

    with open("configs/providers/pricing.csv") as f:
        providers = list(csv.DictReader(f))

    for provider in providers:

        if provider["billing"] != "serverless":
            continue

        if provider["price_status"] == "pending":
            continue

        rate = float(provider["usd_per_hour"])

        for throughput in assumptions['scenarios'].values():
            for cold_start in [0, 5, 15, 30]:
                for idle in [0, 10, 30]:

                    metrics = calculate_serverless_cost(
                        hourly_rate=rate,
                        throughput=throughput,
                        output_tokens=256,
                        cold_start_seconds=cold_start,
                        idle_seconds=idle
                    )

                    results.append({
                        **provider,
                        "measurement_type": "modeled",
                        "assumed_throughput": throughput,
                        "throughput_source": assumptions["source"],
                        "throughput_confidence": assumptions["confidence"],
                        "performance_status": "unmeasured",
                        "cold_start_seconds": cold_start,
                        "idle_seconds": idle,
                        **metrics
                    })

    output = Path("results/serverless-comparison.csv")
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=results[0].keys(), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"PASS: Generated {len(results)} serverless scenarios")
    print(f"Report: {output}")


if __name__ == "__main__":
    main()
