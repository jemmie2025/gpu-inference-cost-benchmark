import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests


def benchmark_request(url, model, prompt, max_tokens):
    started = time.perf_counter()

    response = requests.post(
        f"{url.rstrip('/')}/v1/completions",
        json={
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0,
            "ignore_eos": True
        },
        timeout=180
    )

    response.raise_for_status()
    data = response.json()

    return {
        "latency_seconds": time.perf_counter() - started,
        "input_tokens": data["usage"]["prompt_tokens"],
        "output_tokens": data["usage"]["completion_tokens"]
    }


def run_benchmark(url, model, prompt, max_tokens,
                  concurrency, count):
    started = time.perf_counter()

    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        results = list(pool.map(
            lambda _: benchmark_request(
                url, model, prompt, max_tokens
            ),
            range(count)
        ))

    elapsed = time.perf_counter() - started
    latencies = sorted(r["latency_seconds"] for r in results)
    total_tokens = sum(r["output_tokens"] for r in results)

    return {
        "measurement_type": "measured",
        "model": model,
        "concurrency": concurrency,
        "requests": count,
        "duration_seconds": elapsed,
        "total_input_tokens": sum(
            r["input_tokens"] for r in results
        ),
        "total_output_tokens": total_tokens,
        "output_tokens_per_second": total_tokens / elapsed,
        "requests_per_second": count / elapsed,
        "mean_latency_ms": sum(latencies) / count * 1000,
        "p95_latency_ms": latencies[
            (95 * count + 99) // 100 - 1
        ] * 1000
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000")
    parser.add_argument("--model", required=True)
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--requests", type=int, default=100)
    parser.add_argument("--output-tokens", type=int, default=256)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if min(args.concurrency, args.requests, args.output_tokens) < 1:
        parser.error("Numeric arguments must be positive")

    result = run_benchmark(
        args.url,
        args.model,
        "Explain GPU inference optimization in detail.",
        args.output_tokens,
        args.concurrency,
        args.requests
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2))

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
