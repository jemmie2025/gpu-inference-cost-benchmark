import math


def calculate_cost(hourly_rate, throughput, utilization=1.0,
                   overhead=0.0, hours=730):

    values = [hourly_rate, throughput, utilization,
              overhead, hours]

    if not all(math.isfinite(v) for v in values):
        raise ValueError("Inputs must be finite")

    if hourly_rate <= 0 or throughput <= 0:
        raise ValueError("Rate and throughput must be positive")

    if not 0 < utilization <= 1:
        raise ValueError("Utilization must be between 0 and 1")

    if overhead < 0 or hours <= 0:
        raise ValueError("Invalid overhead or duration")

    effective_rate = hourly_rate * (1 + overhead)
    tokens_per_hour = throughput * utilization * 3600

    return {
        "hourly_cost_usd": round(effective_rate, 6),
        "effective_tokens_per_second": throughput * utilization,
        "tokens_per_hour": tokens_per_hour,
        "cost_per_million_output_tokens": round(
            effective_rate / tokens_per_hour * 1000000, 6
        ),
        "daily_cost_usd": round(effective_rate * 24, 2),
        "monthly_cost_usd": round(effective_rate * hours, 2),
        "idle_cost_per_hour_usd": round(
            effective_rate * (1 - utilization), 6
        )
    }
