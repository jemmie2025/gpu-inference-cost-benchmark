"""Conservative regional and billing-scope pricing normalization."""

import csv
from pathlib import Path

SOURCE = Path("configs/providers/pricing.csv")
OUTPUT = Path("results/normalized-pricing.csv")

REQUIRED = {
    "provider", "instance", "gpu", "gpu_count",
    "region", "billing", "usd_per_hour",
    "price_status", "cost_scope",
    "price_captured_at", "price_source_url",
    "target_market", "regional_price_status",
    "regional_source_url", "regional_ranking_eligible",
}


def normalize(row):
    missing = REQUIRED.difference(row)
    if missing:
        raise ValueError(f"Missing pricing fields: {sorted(missing)}")

    rate = float(row["usd_per_hour"])
    if not 0 < rate < float("inf"):
        raise ValueError("Hourly price must be finite and positive")

    if row["billing"] not in {"on-demand", "spot", "serverless"}:
        raise ValueError("Unsupported billing type")

    if row["target_market"] != "US":
        raise ValueError("Unsupported comparison market")

    reasons = []

    # Instance prices and individual resource charges must not be
    # treated as financially equivalent.
    if row["cost_scope"] != "instance":
        reasons.append("incomplete_or_non_instance_billing_scope")

    if row["region"] == "unspecified":
        reasons.append("provider_region_unconfirmed")

    if row["regional_price_status"] != "regional_published":
        reasons.append("regional_price_not_independently_verified")

    if row["price_status"] != "published":
        reasons.append("base_price_not_independently_verified")

    if row["regional_ranking_eligible"] != "true":
        reasons.append("regional_ranking_not_authorized")

    if row["billing"] == "serverless":
        reasons.append("serverless_billing_policy_not_normalized")

    if row["cost_scope"] != "instance":
        status = "excluded"
    elif not reasons:
        status = "strict_regional_eligible"
    else:
        status = "indicative_only"

    return {
        **row,
        "normalized_usd_per_hour": f"{rate:.6f}",
        "normalization_status": status,
        "normalization_reason": (
            ";".join(reasons) if reasons else "eligible_for_strict_regional_comparison"
        ),
        "regional_price_verified": str(
            row["regional_price_status"] == "regional_published"
            and row["price_status"] == "published"
            and row["region"] != "unspecified"
        ).lower(),
        "total_billing_scope_verified": str(
            row["cost_scope"] == "instance"
        ).lower(),
    }


def main():
    with SOURCE.open(newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [normalize(row) for row in reader]

    if not rows:
        raise ValueError("No pricing records found")

    providers = {row["provider"] for row in rows}
    expected = {
        "AWS", "GCP", "Lambda", "RunPod", "Modal", "Replicate"
    }
    if providers != expected:
        raise ValueError(
            f"Provider coverage mismatch: {providers ^ expected}"
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=rows[0].keys(),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    counts = {
        status: sum(r["normalization_status"] == status for r in rows)
        for status in (
            "strict_regional_eligible",
            "indicative_only",
            "excluded",
        )
    }

    print(f"PASS: Normalized {len(rows)} pricing records")
    for status, count in counts.items():
        print(f"{status}: {count}")
    print(f"Report: {OUTPUT}")


if __name__ == "__main__":
    main()
