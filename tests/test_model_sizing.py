import pytest

from src.model_sizing import (
    estimate_memory,
    check_memory_fit
)


def test_bf16_memory():
    result = estimate_memory(7.61, 16)
    assert result["weight_memory_gib"] == pytest.approx(
        14.175, abs=0.01
    )


def test_quantization():
    bf16 = estimate_memory(8, 16)
    int4 = estimate_memory(8, 4)

    assert int4["weight_memory_gib"] < (
        bf16["weight_memory_gib"]
    )


def test_tensor_parallelism():
    result = estimate_memory(70, 16, 4)
    assert result["required_gpu_count"] == 4
    assert result["estimated_per_gpu_gib"] < 48


def test_memory_fit():
    assert check_memory_fit(15, 24)
    assert not check_memory_fit(30, 24)


@pytest.mark.parametrize("size,bits,tp", [
    (0, 16, 1),
    (-1, 16, 1),
    (7, 3, 1),
    (7, 16, 0)
])
def test_invalid_configuration(size, bits, tp):
    with pytest.raises(ValueError):
        estimate_memory(size, bits, tp)
