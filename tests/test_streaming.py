from unittest.mock import patch, MagicMock
import pytest

from benchmarks.scripts.streaming import measure_streaming


@patch("benchmarks.scripts.streaming.requests.post")
def test_streaming_metrics(mock_post):
    response = MagicMock()
    response.iter_lines.return_value = [
        b'data: {"choices":[{"text":"Hello"}]}',
        b'data: {"choices":[{"text":" world"}]}',
        b'data: {"choices":[],"usage":{"completion_tokens":2}}',
        b'data: [DONE]'
    ]

    mock_post.return_value.__enter__.return_value = response

    result = measure_streaming(
        "http://localhost:8000", "test-model", "Test"
    )

    assert result["ttft_ms"] >= 0
    assert result["output_tokens"] == 2
    assert result["stream_chunks"] == 2
    assert result["mean_inter_chunk_latency_ms"] >= 0


@patch("benchmarks.scripts.streaming.requests.post")
def test_empty_stream(mock_post):
    response = MagicMock()
    response.iter_lines.return_value = [b"data: [DONE]"]

    mock_post.return_value.__enter__.return_value = response

    with pytest.raises(RuntimeError):
        measure_streaming(
            "http://localhost:8000", "test-model", "Test"
        )
