"""Two distinctions the released aggregates conceal, on the released data.

Panel A plots the directional components against each other. The diagonal is
exact cancellation, where improvement and degradation are equal and the signed
change is zero. Distance from the origin is how much items moved; distance from
the diagonal is how much of that movement survived aggregation.

Panel B pairs the change tail with the absolute case-risk tail for the same
comparisons. Both are selection-corrected, so they are comparable: the split
estimator for the change tail, cross-fitting for the case-risk tail. The change
tail varies widely across comparisons while the case-risk tail stays near one,
which is the non-redundancy argued in Section 3.5 shown outside simulation.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import figstyle

HERE = Path(__file__).resolve().parent

MARKERS = {"MMLU-Pro": "o", "GPQA": "s", "HLE": "^", "SimpleQA": "D"}


def build(frame: pd.DataFrame, path: Path) -> None:
    figstyle.setup()
    colors = figstyle.COLORS
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.4))

    # --- A. directional components ------------------------------------------
    ax = axes[0]
    limit = max(frame.f_plus.max(), frame.f_minus.max()) * 1.12
    ax.plot([0, limit], [0, limit], color=colors["light"], linewidth=1.0, zorder=1)
    # Sits on the diagonal past the largest observed degradation, so it can't
    # collide with a point.
    ax.text(
        limit * 0.78, limit * 0.78, "exact cancellation",
        rotation=45, rotation_mode="anchor",
        ha="center", va="bottom", fontsize=7.5, color=colors["dark"],
    )
    for label, marker in MARKERS.items():
        sub = frame[frame.benchmark_label == label]
        ax.scatter(
            sub.f_minus, sub.f_plus, marker=marker, s=26,
            facecolor="none", edgecolor=colors["primary"], linewidth=1.0,
            label=label, zorder=3,
        )
    ax.set_xlabel(r"degradation $F^-$")
    ax.set_ylabel(r"improvement $F^+$")
    ax.set_title("A. Movement in both directions")
    ax.set_xlim(0, limit)
    ax.set_ylim(0, limit)
    ax.set_aspect("equal")
    ax.legend(fontsize=7, handletextpad=0.3, borderpad=0.2, labelspacing=0.25)

    # --- B. change tail against absolute case-risk tail ----------------------
    ax = axes[1]
    ordered = frame.sort_values("split_wtd").reset_index(drop=True)
    x = np.arange(len(ordered))
    ax.vlines(
        x, ordered.split_wtd, ordered.absolute_loss_tail_crossfit,
        color=colors["light"], linewidth=0.9, zorder=1,
    )
    ax.scatter(x, ordered.split_wtd, s=20, color=colors["secondary"],
               label="change tail (split WTD)", zorder=3)
    ax.scatter(x, ordered.absolute_loss_tail_crossfit, s=20, color=colors["primary"],
               label="case-risk tail (cross-fitted WTL)", zorder=3)
    ax.set_xlabel("released comparisons, ordered by change tail")
    ax.set_ylabel("worst-decile value")
    ax.set_title("B. A change tail is not an absolute tail")
    ax.set_ylim(0, 1.05)
    ax.set_xticks([])
    ax.legend(fontsize=7, loc="center left", handletextpad=0.3,
              borderpad=0.2, labelspacing=0.25)

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reanalysis",
        type=Path,
        default=HERE / "outputs" / "zhang_reanalysis" / "main_reanalysis.csv",
    )
    parser.add_argument(
        "--output", type=Path, default=HERE / "outputs" / "hidden_distinctions.pdf"
    )
    args = parser.parse_args()
    frame = pd.read_csv(args.reanalysis)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    build(frame, args.output)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
