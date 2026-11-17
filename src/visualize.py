import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


def main():
    with open("results/utilization-sensitivity.csv") as f:
        rows = list(csv.DictReader(f))

    groups = {}

    for row in rows:
        label = f'{row["provider"]} - {row["gpu"]}'
        groups.setdefault(label, []).append(row)

    fig, ax = plt.subplots(figsize=(10, 6))

    for label, records in groups.items():
        records.sort(key=lambda r: float(r["utilization"]))

        ax.plot(
            [float(r["utilization"]) * 100 for r in records],
            [float(r["cost_per_million_output_tokens"])
             for r in records],
            marker="o",
            linewidth=2,
            label=label
        )

    ax.set_title("GPU Inference Cost vs. Utilization")
    ax.set_xlabel("Workload Utilization (%)")
    ax.set_ylabel("Cost per Million Output Tokens (USD)")
    ax.set_xticks([25, 50, 75, 100])
    ax.grid(alpha=0.25)
    ax.legend()

    fig.text(
        0.5, 0.01,
        "Modeled scenario: 100 output tokens/sec; "
        "additional overhead excluded",
        ha="center",
        fontsize=9
    )

    fig.tight_layout(rect=[0, 0.04, 1, 1])

    output = Path("results/utilization-analysis.png")
    fig.savefig(output, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"PASS: Chart generated at {output}")


if __name__ == "__main__":
    main()
