import json
import time

import requests


def measure_streaming(url, model, prompt, max_tokens=256):
    started = time.perf_counter()
    timestamps = []
    output_tokens = None

    with requests.post(
        f"{url.rstrip('/')}/v1/completions",
        json={
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0,
            "stream": True,
            "stream_options": {"include_usage": True}
        },
        stream=True,
        timeout=180
    ) as response:
        response.raise_for_status()

        for line in response.iter_lines(chunk_size=1):
            if not line.startswith(b"data: "):
                continue

            payload = line[6:]

            if payload == b"[DONE]":
                break

            data = json.loads(payload)

            if data.get("usage"):
                output_tokens = data["usage"]["completion_tokens"]

            choices = data.get("choices", [])

            if choices and choices[0].get("text"):
                timestamps.append(time.perf_counter())

    if not timestamps:
        raise RuntimeError("No generated content received")

    duration = time.perf_counter() - started

    return {
        "ttft_ms": (timestamps[0] - started) * 1000,
        "stream_latency_ms": duration * 1000,
        "mean_inter_chunk_latency_ms": (
            (timestamps[-1] - timestamps[0])
            / (len(timestamps) - 1) * 1000
            if len(timestamps) > 1 else None
        ),
        "output_tokens": output_tokens,
        "stream_chunks": len(timestamps)
    }
