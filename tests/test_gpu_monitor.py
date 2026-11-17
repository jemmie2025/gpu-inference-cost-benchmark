from unittest.mock import patch
from benchmarks.scripts.gpu_monitor import collect_gpu_metrics


@patch("benchmarks.scripts.gpu_monitor.subprocess.run")
def test_gpu_unavailable(mock_run):
    mock_run.side_effect = FileNotFoundError("nvidia-smi")

    result = collect_gpu_metrics()

    assert result["status"] == "unavailable"
    assert result["metrics"] == []


@patch("benchmarks.scripts.gpu_monitor.subprocess.run")
def test_gpu_available(mock_run):
    mock_run.return_value.stdout = (
        "0, NVIDIA L40S, 46068, 18000, 85, 250, 65\n"
    )

    result = collect_gpu_metrics()

    assert result["status"] == "available"
    assert result["metrics"][0]["gpu_name"] == "NVIDIA L40S"
