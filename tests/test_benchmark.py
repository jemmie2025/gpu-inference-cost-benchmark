from unittest.mock import patch, Mock

from benchmarks.scripts.benchmark import (
    benchmark_request,
    run_benchmark
)


@patch("benchmarks.scripts.benchmark.requests.post")
def test_benchmark_request(mock_post):
    response = Mock()
    response.json.return_value = {
        "usage": {
            "prompt_tokens": 512,
            "completion_tokens": 256
        }
    }
    mock_post.return_value = response

    result = benchmark_request(
        "http://localhost:8000",
        "test-model",
        "Test prompt",
        256
    )

    assert result["input_tokens"] == 512
    assert result["output_tokens"] == 256
    assert result["latency_seconds"] >= 0


@patch("benchmarks.scripts.benchmark.benchmark_request")
def test_concurrent_benchmark(mock_request):
    mock_request.return_value = {
        "input_tokens": 512,
        "output_tokens": 256,
        "latency_seconds": 0.1
    }

    result = run_benchmark(
        "http://localhost:8000",
        "test-model",
        "Test prompt",
        256,
        8,
        16
    )

    assert result["requests"] == 16
    assert result["total_output_tokens"] == 4096
    assert result["total_input_tokens"] == 8192
    assert result["output_tokens_per_second"] > 0
    assert result["p95_latency_ms"] == 100
