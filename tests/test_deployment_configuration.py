import json
from pathlib import Path

import yaml


EXPECTED_IMAGE = "vllm/vllm-openai:v0.33.0"
EXPECTED_MODEL = "Qwen/Qwen3-8B"


def test_compose_version_pinned():
    config = yaml.safe_load(
        Path("infrastructure/docker/compose.yaml").read_text()
    )

    service = config["services"]["inference"]

    assert service["image"] == EXPECTED_IMAGE
    assert EXPECTED_MODEL in service["command"]


def test_kubernetes_version_pinned():
    documents = list(yaml.safe_load_all(
        Path("infrastructure/kubernetes/inference.yaml").read_text()
    ))

    deployment = next(
        d for d in documents
        if d["kind"] == "Deployment"
    )

    container = deployment["spec"]["template"]["spec"]["containers"][0]

    assert container["image"] == EXPECTED_IMAGE
    assert EXPECTED_MODEL in container["args"]


def test_environment_version_consistent():
    content = Path(
        "infrastructure/docker/.env.example"
    ).read_text().strip()

    assert content == f"VLLM_IMAGE={EXPECTED_IMAGE}"


def test_model_portfolio_modernized():
    models = [
        json.loads(path.read_text())
        for path in Path("configs/models").glob("*.json")
    ]

    ids = {model["model_id"] for model in models}

    assert len(ids) == 5
    assert "Qwen/Qwen3-8B" in ids
    assert "Qwen/Qwen3-32B-AWQ" in ids
    assert not any("qwen2.5" in m.lower() for m in ids)


def test_unavailable_recommendations_have_no_price():
    from src.recommendations import generate_recommendations

    for row in generate_recommendations():
        if row["provider"] == "No eligible priced configuration":
            assert row["cost_per_million_output_tokens"] == "N/A"


def test_unique_recommendations():
    from src.recommendations import generate_recommendations

    rows = generate_recommendations()
    cases = [row["use_case"] for row in rows]

    assert len(cases) == len(set(cases)) == 7
