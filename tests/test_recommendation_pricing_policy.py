from pathlib import Path

import pytest

from src.recommendations import (
    eligible_candidates,
    pricing_index,
    pricing_key,
)


def test_normalized_pricing_available():
    assert Path("results/normalized-pricing.csv").is_file()
    assert len(pricing_index()) == 12


def test_pricing_identity():
    row = {
        "provider": "GCP",
        "instance": "g2-standard-12",
        "gpu": "L4",
        "billing": "on-demand",
        "region": "us-central1",
    }

    assert len(pricing_key(row)) == 5


def test_excluded_price_cannot_win():
    policy = next(
        row for row in pricing_index().values()
        if row["normalization_status"] == "excluded"
    )

    candidate = {
        **policy,
        "cost_per_million_output_tokens": "0.000001",
    }

    assert eligible_candidates(
        [candidate], pricing_index()
    ) == []


def test_missing_price_rejected():
    candidate = {
        "provider": "Unknown",
        "instance": "unknown",
        "gpu": "L4",
        "billing": "on-demand",
        "region": "unknown",
        "cost_scope": "instance",
    }

    with pytest.raises(ValueError, match="Missing normalized pricing"):
        eligible_candidates([candidate], pricing_index())


def test_strict_region_precedes_cheaper_indicative():
    from src.recommendations import choose_winner

    pricing = pricing_index()

    strict = next(
        row for row in pricing.values()
        if row["normalization_status"] == "strict_regional_eligible"
        and row["billing"] == "on-demand"
    )

    indicative = next(
        row for row in pricing.values()
        if row["normalization_status"] == "indicative_only"
        and row["billing"] == "on-demand"
        and row["cost_scope"] == "instance"
    )

    candidates = [
        {
            **strict,
            "cost_per_million_output_tokens": "10.00",
        },
        {
            **indicative,
            "cost_per_million_output_tokens": "0.01",
        },
    ]

    winner, status = choose_winner(candidates, pricing)

    assert pricing_key(winner) == pricing_key(strict)
    assert status == "US-regional modeled winner"
