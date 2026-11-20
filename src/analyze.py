import csv
import json
from pathlib import Path

from src.cost_engine import calculate_cost


def main():
    config = json.loads(
        Path("configs/workloads/performance-assumptions.json").read_text()
    )
    assumptions = config["throughput"]

    billing = json.loads(
        Path("configs/providers/billing.json").read_text()
    )

    results = []

    with open("configs/providers/pricing.csv") as f:
        providers = list(csv.DictReader(f))

    for provider in providers:

        if provider["price_status"] == "pending":
            continue

        if provider["billing"] == "serverless":
            continue

        rate = float(provider["usd_per_hour"])

        for throughput in assumptions['scenarios'].values():
            for utilization in billing["analysis"]["utilization_levels"]:
                for overhead in config["infrastructure_overhead"]["scenarios"]:

                    metrics = calculate_cost(
                        rate, throughput, utilization, overhead
                    )

                    results.append({
                        **provider,
                        "measurement_type": "modeled",
                        "assumed_throughput": throughput,
                        "throughput_source": assumptions["source"],
                        "throughput_confidence": assumptions["confidence"],
                        "performance_status": "unmeasured",
                        "utilization": utilization,
                        "overhead": overhead,
                        "overhead_source": config["infrastructure_overhead"]["source"],
                        "overhead_source_url": config["infrastructure_overhead"]["supporting_source_url"],
                        **metrics
                    })

    output = Path("results/cost-comparison.csv")
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)

    print(f"PASS: Generated {len(results)} cost scenarios")
    print(f"Report: {output}")


if __name__ == "__main__":
    main()
