"""Four item-level states behind one stable mean.

A constructed illustration, not data. Each column is a different distribution of
per-item change with the same near-zero mean. The top row shows that change
distribution; the bottom row shows the resulting worst-decile absolute case
risk. Columns one and four are indistinguishable in the top row and differ
sharply in the bottom one, which is why a change statistic can't stand in for an
absolute risk measure.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from . import figstyle

HERE = Path(__file__).resolve().parent

N = 600
Q = 0.10


def states(rng: np.random.Generator) -> list[dict]:
    """Construct four change distributions with matched means."""
    zero = np.zeros(N)

    # 1. nothing moves, and baseline performance is high
    high_base = rng.uniform(0.80, 1.0, size=N)

    # 2. gains and losses cancel
    cancel = rng.normal(0.0, 0.16, size=N)

    # 3. most items steady, a tenth collapse
    concentrated = np.zeros(N)
    hit = rng.choice(N, size=N // 10, replace=False)
    concentrated[hit] = -0.55
    concentrated -= concentrated.mean()  # match the others at zero mean

    # 4. nothing moves, but a tenth were already failing
    persistent_base = rng.uniform(0.80, 1.0, size=N)
    persistent_base[rng.choice(N, size=N // 10, replace=False)] = rng.uniform(
        0.0, 0.08, size=N // 10
    )

    return [
        {"label": "unchanged", "delta": zero, "level": high_base},
        {"label": "gains and losses\ncancel", "delta": cancel, "level": high_base + cancel},
        {"label": "deterioration\nconcentrated", "delta": concentrated, "level": high_base + concentrated},
        {"label": "stable severe\nfailure", "delta": zero, "level": persistent_base},
    ]


def worst_decile_loss(level: np.ndarray) -> float:
    loss = np.clip(1.0 - level, 0.0, 1.0)
    k = max(1, int(np.ceil(Q * loss.size)))
    return float(np.sort(loss)[-k:].mean())


def build(path: Path, seed: int = 20260722) -> None:
    figstyle.setup(font_size=8.5, title_size=9.0, tick_size=7.5)
    colors = figstyle.COLORS
    rng = np.random.default_rng(seed)
    panels = states(rng)

    fig, axes = plt.subplots(2, 4, figsize=(7.4, 3.5),
                             gridspec_kw={"height_ratios": [2.0, 1.0]})

    for col, panel in enumerate(panels):
        ax = axes[0, col]
        ax.hist(panel["delta"], bins=np.linspace(-0.7, 0.7, 33),
                color=colors["primary"], edgecolor="none")
        ax.axvline(0.0, color=colors["light"], linewidth=0.8, zorder=0)
        ax.set_xlim(-0.7, 0.7)
        ax.set_ylim(0, N * 1.05)
        ax.set_yticks([])
        ax.set_xticks([-0.5, 0.0, 0.5])
        ax.set_title(panel["label"], fontsize=8.5)
        mean_delta = float(panel["delta"].mean())
        # Left-aligned: every distribution spikes at or near zero.
        ax.text(0.04, 0.88, f"mean {mean_delta:+.2f}", transform=ax.transAxes,
                ha="left", fontsize=7.5, color=colors["dark"])
        ax.set_xlabel("per-item change", fontsize=7.5)
        if col == 0:
            ax.set_ylabel("items")

        ax = axes[1, col]
        value = worst_decile_loss(panel["level"])
        ax.barh([0], [value], height=0.55, color=colors["secondary"])
        ax.set_xlim(0, 1.2)
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([])
        ax.set_xticks([0, 0.5, 1.0])
        ax.text(value + 0.04, 0, f"{value:.2f}",
                va="center", fontsize=7.5, color=colors["dark"])
        if col == 0:
            ax.set_ylabel("worst-decile\nabsolute loss", fontsize=7.5)

    fig.tight_layout()
    fig.subplots_adjust(hspace=0.75)
    fig.savefig(path)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=HERE / "outputs" / "stable_mean_states.pdf")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    build(args.output)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
