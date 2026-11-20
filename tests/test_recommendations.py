import csv
from pathlib import Path

from src.recommendations import (
    cheapest,
    generate_recommendations
)


def test_cheapest_candidate():
    rows = [
        {"cost_per_million_output_tokens": "10"},
        {"cost_per_million_output_tokens": "5"}
    ]

    assert cheapest(rows) == rows[1]


def test_empty_candidates():
    assert cheapest([]) is None


def test_recommendation_coverage():
    rows = generate_recommendations()

    assert len(rows) == 7
    assert all(r["provider"] for r in rows)
    assert all(r["model"] for r in rows)


def test_regional_winners_have_region():
    for row in generate_recommendations():
        if row["status"] == "US-regional modeled winner":
            assert row["region"] != "unspecified"


def test_no_fabricated_70b_cost():
    row = next(
        r for r in generate_recommendations()
        if "70B" in r["use_case"]
    )

    assert row["cost_per_million_output_tokens"] == "N/A"


def test_recommendation_artifacts():
    assert Path("results/recommendations.md").is_file()

    with open("results/recommendations.csv") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 7
