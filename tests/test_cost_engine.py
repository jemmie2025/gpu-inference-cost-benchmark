import pytest

from src.cost_engine import calculate_cost


def test_cost_per_million():
    result = calculate_cost(1.0, 100)
    assert result["cost_per_million_output_tokens"] == pytest.approx(
        2.777778
    )


def test_utilization():
    result = calculate_cost(1.0, 100, 0.5)
    assert result["cost_per_million_output_tokens"] == pytest.approx(
        5.555556
    )


def test_overhead():
    result = calculate_cost(1.0, 100, overhead=0.2)
    assert result["hourly_cost_usd"] == 1.2


def test_monthly_cost():
    result = calculate_cost(1.0, 100)
    assert result["monthly_cost_usd"] == 730


def test_idle_cost():
    result = calculate_cost(1.0, 100, 0.25)
    assert result["idle_cost_per_hour_usd"] == 0.75


@pytest.mark.parametrize("rate,throughput,utilization", [
    (0, 100, 1),
    (1, 0, 1),
    (1, 100, 0),
    (1, 100, 1.5),
    (-1, 100, 1)
])
def test_invalid_inputs(rate, throughput, utilization):
    with pytest.raises(ValueError):
        calculate_cost(rate, throughput, utilization)
