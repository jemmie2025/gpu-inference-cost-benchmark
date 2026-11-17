import csv
from pathlib import Path


def main():
    with open("results/cost-comparison.csv") as f:
        rows = list(csv.DictReader(f))

    selected = [
        row for row in rows
        if float(row["assumed_throughput"]) == 100
        and float(row["overhead"]) == 0
        and row["price_status"] == "published"
        and row["cost_scope"] == "instance"
    ]

    selected.sort(
        key=lambda row: (
            row["provider"],
            row["instance"],
            float(row["utilization"])
        )
    )

    fields = [
        "provider",
        "instance",
        "gpu",
        "billing",
        "measurement_type",
        "assumed_throughput",
        "utilization",
        "hourly_cost_usd",
        "cost_per_million_output_tokens",
        "monthly_cost_usd"
    ]

    output = Path("results/utilization-sensitivity.csv")

    with output.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fields,
            extrasaction="ignore",
            lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(selected)

    print(f"PASS: Generated {len(selected)} sensitivity scenarios")
    print(f"Report: {output}")


if __name__ == "__main__":
    main()
