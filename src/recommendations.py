import csv
from pathlib import Path


def read_rows(filename):
    with open(filename) as f:
        return list(csv.DictReader(f))


def cheapest(rows):
    return min(
        rows,
        key=lambda r: float(r["cost_per_million_output_tokens"]),
        default=None
    )


PRICING_KEYS = ("provider", "instance", "gpu", "billing", "region")


def pricing_key(row):
    return tuple(row[key] for key in PRICING_KEYS)


def pricing_index():
    rows = read_rows("results/normalized-pricing.csv")
    index = {}

    for row in rows:
        key = pricing_key(row)
        if key in index:
            raise ValueError(f"Duplicate pricing configuration: {key}")
        index[key] = row

    return index


def eligible_candidates(rows, pricing):
    accepted = []

    for row in rows:
        policy = pricing.get(pricing_key(row))

        if policy is None:
            raise ValueError(
                f"Missing normalized pricing for {pricing_key(row)}"
            )

        if row["cost_scope"] != policy["cost_scope"]:
            raise ValueError("Billing-scope mismatch")

        if policy["normalization_status"] == "excluded":
            continue

        accepted.append(row)

    return accepted


def choose_winner(candidates, pricing):
    """Select using normalized billing and regional eligibility."""
    candidates = eligible_candidates(candidates, pricing)

    strict = [
        row for row in candidates
        if pricing[pricing_key(row)]["normalization_status"]
        == "strict_regional_eligible"
    ]

    if strict:
        return cheapest(strict), "US-regional modeled winner"

    if candidates:
        return (
            cheapest(candidates),
            "Indicative; regional quote required"
        )

    return None, "No eligible normalized pricing"


def generate_recommendations():
    pricing = pricing_index()
    pricing = pricing_index()
    models = read_rows("results/model-cost-comparison.csv")
    serverless = read_rows("results/serverless-comparison.csv")
    compatibility = read_rows("results/model-compatibility.csv")

    reference = [
        r for r in models
        if float(r["assumed_throughput"]) == 100
        and float(r["utilization"]) == 0.75
    ]

    use_cases = [
        (
            "Lightweight classification and routing",
            "Qwen/Qwen3-0.6B",
            "on-demand"
        ),
        (
            "Continuous general-purpose inference",
            "Qwen/Qwen3-8B",
            "on-demand"
        ),
        (
            "Lightweight interruption-tolerant batch inference",
            "Qwen/Qwen3-0.6B",
            "spot"
        ),
        (
            "Memory-efficient 8B inference",
            "hugging-quants/Meta-Llama-3.1-8B-Instruct-AWQ-INT4",
            "on-demand"
        ),
        (
            "Quantized large-model inference",
            "Qwen/Qwen3-32B-AWQ",
            "on-demand"
        )
    ]

    recommendations = []

    for use_case, model, billing in use_cases:
        candidates = eligible_candidates([
            r for r in reference
            if r["model"] == model
            and r["billing"] == billing
        ], pricing)

        winner, status = choose_winner(candidates, pricing)

        if winner:
            recommendations.append({
                "use_case": use_case,
                "provider": winner["provider"],
                "model": model,
                "gpu": winner["gpu"],
                "billing": billing,
                "region": winner["region"],
                "cost_per_million_output_tokens":
                    winner["cost_per_million_output_tokens"],
                "status": status
            })


        else:
            recommendations.append({
                "use_case": use_case,
                "provider": "No eligible priced configuration",
                "model": model,
                "gpu": "N/A",
                "billing": billing,
                "region": "Pending",
                "cost_per_million_output_tokens": "N/A",
                "status": "Compatible GPU and pricing verification required"
            })

    candidates = [
        r for r in serverless
        if float(r["assumed_throughput"]) == 100
        and float(r["cold_start_seconds"]) == 5
        and float(r["idle_seconds"]) == 0
        and r["price_status"] == "published"
        and r["gpu"] == "L40S"
        and r["cost_scope"] == "instance"
    ]

    candidates = eligible_candidates(candidates, pricing)
    candidates = eligible_candidates(candidates, pricing)
    winner = cheapest(candidates)

    if winner:
        recommendations.append({
            "use_case": "Intermittent serverless inference",
            "provider": winner["provider"],
            "model": "Qwen/Qwen3-8B",
            "gpu": winner["gpu"],
            "billing": "serverless",
            "region": winner["region"],
            "cost_per_million_output_tokens":
                winner["cost_per_million_output_tokens"],
            "status": "Indicative hardware-rate estimate; model deployment unverified"
        })

    recommendations.append({
        "use_case": "70B multi-GPU inference",
        "provider": "No eligible priced configuration",
        "model": "meta-llama/Llama-3.3-70B-Instruct",
        "gpu": "4 x A100 80GB or H100 80GB",
        "billing": "on-demand",
        "region": "Pending",
        "cost_per_million_output_tokens": "N/A",
        "status": "Multi-GPU quotation and runtime validation required"
    })

    return recommendations


def main():
    rows = generate_recommendations()

    output = Path("results/recommendations.csv")

    with output.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=rows[0].keys(),
            lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)

    report = [
        "# Workload-Specific Recommendations",
        "",
        "Dedicated reference: 100 assumed output tokens/sec,",
        "75% utilization and zero additional cost overhead.",
        "",
        "Serverless reference: 256 output tokens, 100 assumed",
        "tokens/sec, five-second cold start and zero idle time.",
        "",
        "| Use case | Provider | Model | GPU | USD/M tokens | Status |",
        "|---|---|---|---|---:|---|"
    ]

    for row in rows:
        cost = row["cost_per_million_output_tokens"]

        if cost != "N/A":
            cost = f"{float(cost):.2f}"

        report.append(
            f'| {row["use_case"]} | {row["provider"]} | '
            f'{row["model"]} | {row["gpu"]} | '
            f'{cost} | {row["status"]} |'
        )

    report.extend([
        "",
        "## Interpretation",
        "",
        "- Regional candidates take precedence over unconfirmed rates.",
        "- Indicative winners are not verified US-region winners.",
        "- Model selection reflects intended workload and estimated memory fit.",
        "- Model quality, latency and throughput have not been benchmarked.",
        "- Spot capacity requires interruption handling.",
        "- Serverless estimates exclude incompatible billing scopes.",
        "- No provider winner is declared for the 70B configuration.",
        "- Refresh prices and measure performance before procurement."
    ])

    Path("results/recommendations.md").write_text(
        "\n".join(report) + "\n"
    )

    print(f"PASS: Generated {len(rows)} workload recommendations")


if __name__ == "__main__":
    main()
