import csv
from pathlib import Path


def main():
    with open("results/utilization-sensitivity.csv") as f:
        rows = list(csv.DictReader(f))

    selected = [
        r for r in rows
        if float(r["utilization"]) == 0.5
    ]

    selected.sort(
        key=lambda r: float(
            r["cost_per_million_output_tokens"]
        )
    )

    report = [
        "# GPU Cost Comparison",
        "",
        "## Indicative Dedicated GPU Economics",
        "",
        "Modeled workload: 100 output tokens/sec, "
        "50% utilization, excluding additional overhead.",
        "",
        "| Provider | GPU | Billing | Region | Regional status | Price captured | USD/hour | USD/M tokens | Monthly USD |",
        "|---|---|---|---|---|---|---:|---:|---:|"
    ]

    for r in selected:
        report.append(
            f'| {r["provider"]} | {r["gpu"]} | '
            f'{r["billing"]} | {r["region"]} | '
            f'{r["regional_price_status"]} | {r["price_captured_at"]} | '
            f'{float(r["hourly_cost_usd"]):.2f} | '
            f'{float(r["cost_per_million_output_tokens"]):.2f} | '
            f'{float(r["monthly_cost_usd"]):.2f} |'
        )

    report.extend([
        "",
        "## Utilization Analysis",
        "",
        "![Utilization Analysis](utilization-analysis.png)",
        "",
        "## Limitations",
        "",
        "- Throughput values are modeled assumptions.",
        "- Secondary-source prices are excluded from this indicative table.",
        "- Region-unconfirmed rates are indicative only.",
        "- Strict US-region winners require regional pricing eligibility.",
        "- Serverless economics are reported separately.",
        "- Live GPU performance remains unverified."
    ])

    output = Path("results/provider-comparison.md")
    output.write_text("\n".join(report) + "\n")

    print(f"PASS: Report generated at {output}")


if __name__ == "__main__":
    main()
