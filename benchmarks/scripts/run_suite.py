import argparse
import json
from pathlib import Path

from benchmark import run_benchmark
from streaming import measure_streaming
from gpu_monitor import collect_gpu_metrics

parser = argparse.ArgumentParser()
parser.add_argument("--url", default="http://localhost:8000")
parser.add_argument(
    "--model-config",
    default="configs/models/qwen-7b.json"
)
args = parser.parse_args()

model = json.loads(
    Path(args.model_config).read_text()
)

workload = json.loads(
    Path("configs/workloads/baseline.json").read_text()
)

output = Path("benchmarks/raw") / Path(args.model_config).stem
output.mkdir(parents=True, exist_ok=True)

prompt = "Explain GPU inference optimization in detail."

for concurrency in workload["concurrency_levels"]:

    run_benchmark(
        args.url,
        model["model_id"],
        prompt,
        workload["output_tokens"],
        concurrency,
        workload["warmup_requests"]
    )

    for repetition in range(workload["repetitions"]):
        result = run_benchmark(
            args.url,
            model["model_id"],
            prompt,
            workload["output_tokens"],
            concurrency,
            workload["benchmark_requests"]
        )

        result["repetition"] = repetition + 1
        result["gpu_telemetry_snapshot"] = collect_gpu_metrics()
        result["streaming_probe"] = measure_streaming(
            args.url,
            model["model_id"],
            prompt,
            workload["output_tokens"]
        )
        result["streaming_probe_concurrency"] = 1

        filename = output / (
            f"c{concurrency}-run{repetition + 1}.json"
        )

        filename.write_text(json.dumps(result, indent=2))
        print(f"Completed: {filename}")
