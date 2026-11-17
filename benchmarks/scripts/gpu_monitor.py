import csv
import subprocess


def collect_gpu_metrics():
    command = [
        "nvidia-smi",
        "--query-gpu=index,name,memory.total,memory.used,"
        "utilization.gpu,power.draw,temperature.gpu",
        "--format=csv,noheader,nounits"
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )

        fields = [
            "gpu_index",
            "gpu_name",
            "memory_total_mb",
            "memory_used_mb",
            "utilization_percent",
            "power_watts",
            "temperature_celsius"
        ]

        return {
            "status": "available",
            "metrics": list(csv.DictReader(
                result.stdout.splitlines(),
                fieldnames=fields,
                skipinitialspace=True
            ))
        }

    except (
        FileNotFoundError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired
    ) as error:
        return {
            "status": "unavailable",
            "reason": str(error),
            "metrics": []
        }


if __name__ == "__main__":
    import json
    print(json.dumps(collect_gpu_metrics(), indent=2))
