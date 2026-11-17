import csv
import json
from pathlib import Path

from src.cost_engine import calculate_cost


def main():
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

        for throughput in [50, 100, 200]:
            for utilization in billing["analysis"]["utilization_levels"]:
                for overhead in billing["analysis"]["overhead_scenarios"]:

                    metrics = calculate_cost(
                        rate, throughput, utilization, overhead
                    )

                    results.append({
                        **provider,
                        "measurement_type": "modeled",
                        "assumed_throughput": throughput,
                        "utilization": utilization,
                        "overhead": overhead,
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
