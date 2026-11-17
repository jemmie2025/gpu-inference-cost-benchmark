import pytest

from src.serverless import calculate_serverless_cost


def test_baseline():
    result = calculate_serverless_cost(3.60, 100, 1000)
    assert result["cost_per_million_output_tokens"] == 10


def test_cold_start():
    result = calculate_serverless_cost(
        3.60, 100, 1000, cold_start_seconds=10
    )
    assert result["cost_per_million_output_tokens"] == 20


def test_idle_billing():
    result = calculate_serverless_cost(
        3.60, 100, 1000, idle_seconds=5
    )
    assert result["billable_seconds"] == 15


def test_additional_cost():
    result = calculate_serverless_cost(
        3.60, 100, 1000, additional_hourly_cost=3.60
    )
    assert result["cost_per_million_output_tokens"] == 20


def test_invalid_throughput():
    with pytest.raises(ValueError):
        calculate_serverless_cost(1, 0)
