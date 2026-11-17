import math


def calculate_serverless_cost(
    hourly_rate,
    throughput,
    output_tokens=256,
    cold_start_seconds=0,
    idle_seconds=0,
    additional_hourly_cost=0
):
    values = [
        hourly_rate, throughput, output_tokens,
        cold_start_seconds, idle_seconds,
        additional_hourly_cost
    ]

    if not all(math.isfinite(v) for v in values):
        raise ValueError("Inputs must be finite")

    if min(hourly_rate, throughput, output_tokens) <= 0:
        raise ValueError("Inputs must be positive")

    if min(cold_start_seconds, idle_seconds,
           additional_hourly_cost) < 0:
        raise ValueError("Costs and durations cannot be negative")

    generation_seconds = output_tokens / throughput

    billable_seconds = (
        generation_seconds
        + cold_start_seconds
        + idle_seconds
    )

    total_rate = hourly_rate + additional_hourly_cost
    request_cost = total_rate / 3600 * billable_seconds

    return {
        "generation_seconds": generation_seconds,
        "billable_seconds": billable_seconds,
        "cost_per_request_usd": round(request_cost, 8),
        "cost_per_million_output_tokens": round(
            request_cost / output_tokens * 1000000, 6
        )
    }
