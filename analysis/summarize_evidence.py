"""Build the compact table, figure, and exact-claim JSON used at handoff."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .metrics import json_safe


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "outputs"


def row_dict(frame: pd.DataFrame, **query: str) -> dict:
    selected = frame
    for key, value in query.items():
        selected = selected[selected[key] == value]
    if len(selected) != 1:
        raise ValueError(f"Expected one row for {query}; found {len(selected)}")
    return selected.iloc[0].to_dict()


def evidence_summary(root: Path) -> dict:
    released = pd.read_csv(root / "zhang_reanalysis" / "main_reanalysis.csv")
    sensitivity = pd.read_csv(root / "zhang_reanalysis" / "trial_tail_sensitivity.csv")
    simulation = pd.read_csv(root / "instability" / "known_truth_summary.csv")
    absolute = pd.read_csv(root / "instability" / "absolute_tail_examples.csv")
    profile = pd.read_csv(root / "profile_correlation" / "profile_correlation_summary.csv")

    reproduction = {}
    for metric in ("baseline_accuracy", "signed_delta", "ins_adjusted", "wtd_adjusted"):
        difference = released[f"{metric}_difference_from_published"].abs()
        reproduction[metric] = {
            "mean_absolute_difference": float(difference.mean()),
            "maximum_absolute_difference": float(difference.max()),
            "maximum_difference_cell": str(released.loc[difference.idxmax(), "cell"]),
        }
    split_gap = released["split_wtd"] - released["wtd_adjusted"]
    q10 = sensitivity[np.isclose(sensitivity["tail_q"], 0.10)]
    sensitivity_medians = q10.groupby("n_trials")[[
        "ins_adjusted", "wtd_adjusted", "wtd_split"
    ]].median()
    sensitivity_sd = (
        q10.groupby(["cell", "n_trials"])[["ins_adjusted", "wtd_adjusted", "wtd_split"]]
        .std()
        .groupby("n_trials")
        .median()
    )
    central = row_dict(released, cell="mmlu_pro.gpt54")
    null_ins = row_dict(simulation, scenario="null_effect", metric="ins", estimator="adjusted")
    null_wtd = row_dict(simulation, scenario="null_effect", metric="wtd", estimator="adjusted")
    null_split = row_dict(
        simulation, scenario="null_effect", metric="wtd", estimator="split_oracle_comparison"
    )
    sparse_split_selected = row_dict(
        simulation, scenario="sparse_collapse", metric="wtd", estimator="split"
    )
    stable_poor = row_dict(absolute, case="stable_poor")
    moderate = row_dict(profile, scenario="moderate_transport")
    low_spread = row_dict(profile, scenario="low_spread")
    flat = row_dict(profile, scenario="flat_perturbed")
    return {
        "released_data": {
            "cells": int(len(released)),
            "reproduction_against_rounded_paper_table": reproduction,
            "mmlu_pro_gpt54": {
                key: central[key] for key in (
                    "n_items", "baseline_accuracy", "perturbed_accuracy", "signed_delta",
                    "ins_raw", "ins_floor", "ins_adjusted", "wtd_raw", "wtd_floor",
                    "wtd_adjusted", "split_wtd", "selection_half_wtd", "split_half_r",
                    "spearman_brown_reliability",
                )
            },
            "split_minus_floor_adjusted_wtd": {
                "split_larger_cells": int((split_gap > 0).sum()),
                "split_smaller_cells": int((split_gap < 0).sum()),
                "mean_difference": float(split_gap.mean()),
                "median_difference": float(split_gap.median()),
                "minimum_difference": float(split_gap.min()),
                "maximum_difference": float(split_gap.max()),
            },
            "median_split_half_r_by_benchmark": released.groupby("benchmark")["split_half_r"].median().to_dict(),
            "trial_sensitivity_at_q10": {
                str(int(n_trials)): {
                    "median_estimates": sensitivity_medians.loc[n_trials].to_dict(),
                    "median_within_cell_subsample_sd": {
                        key: value for key, value in sensitivity_sd.loc[n_trials].to_dict().items()
                        if math.isfinite(value)
                    },
                }
                for n_trials in sensitivity_medians.index
            },
        },
        "known_truth_simulation": {
            "null_effect_adjusted_ins": {
                "truth": null_ins["truth"], "mean": null_ins["estimate_mean"],
                "negative_rate": null_ins["negative_rate"],
            },
            "null_effect_adjusted_wtd": {
                "truth": null_wtd["truth"], "mean": null_wtd["estimate_mean"],
                "negative_rate": null_wtd["negative_rate"],
            },
            "null_effect_split_wtd": {
                "truth": null_split["truth"], "mean": null_split["estimate_mean"],
                "negative_rate": null_split["negative_rate"],
            },
            "sparse_collapse_split_selected_set": {
                "selected_set_truth_mean": sparse_split_selected["truth"],
                "split_estimate_mean": sparse_split_selected["estimate_mean"],
                "bias": sparse_split_selected["bias"],
                "oracle_tail_truth": 0.55,
            },
            "stable_poor": {
                key: stable_poor[key] for key in (
                    "true_wtd", "true_absolute_loss_tail", "observed_wtd_split",
                    "observed_absolute_loss_tail_crossfit",
                )
            },
        },
        "ten_domain_profile_correlation_simulation": {
            "moderate_transport": {
                key: moderate[key] for key in (
                    "true_r", "mean_observed_r", "rmse_observed_r",
                    "nested_bootstrap_coverage", "nested_bootstrap_mean_width",
                )
            },
            "same_r_low_profile_spread": {
                key: low_spread[key] for key in (
                    "true_r", "mean_observed_r", "rmse_observed_r",
                    "nested_bootstrap_coverage", "nested_bootstrap_mean_width",
                )
            },
            "flat_perturbed_profile": {
                "true_r": flat["true_r"],
                "mean_observed_r_from_sampling_noise": flat["mean_observed_r"],
                "sd_observed_r": flat["sd_observed_r"],
            },
        },
    }


def compact_table(root: Path) -> pd.DataFrame:
    released = pd.read_csv(root / "zhang_reanalysis" / "main_reanalysis.csv")
    selected = {"mmlu_pro.gpt54"}
    selected.update(released.loc[released.groupby("benchmark")["wtd_adjusted"].idxmax(), "cell"])
    columns = [
        "cell", "benchmark_label", "model_label", "signed_delta",
        "ins_raw", "ins_floor", "ins_adjusted", "wtd_raw", "wtd_floor",
        "wtd_adjusted", "split_wtd",
    ]
    return released[released["cell"].isin(selected)][columns].sort_values(["benchmark_label", "model_label"])


def write_table_tex(frame: pd.DataFrame, path: Path) -> None:
    def signed(value: float) -> str:
        return f"{0.0 if abs(value) < 0.0005 else value:+.3f}"

    lines = [
        "% Generated by python -m analysis.summarize_evidence; do not edit by hand.",
        "\\begin{tabular}{llrrrrrrrr}",
        "\\toprule",
        "Benchmark & Model & $\\Delta$ & raw INS & pseudo-null & pseudo-null-adj. & raw WTD & pseudo-null & pseudo-null-adj. & split WTD \\\\",
        "\\midrule",
    ]
    for row in frame.itertuples(index=False):
        lines.append(
            f"{row.benchmark_label} & {row.model_label} & {signed(row.signed_delta)} & "
            f"{row.ins_raw:.3f} & {row.ins_floor:.3f} & {row.ins_adjusted:.3f} & "
            f"{row.wtd_raw:.3f} & {row.wtd_floor:.3f} & {row.wtd_adjusted:.3f} & "
            f"{row.split_wtd:.3f} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}", ""])
    path.write_text("\n".join(lines))


def plot_compact(root: Path, path: Path) -> None:
    released = pd.read_csv(root / "zhang_reanalysis" / "main_reanalysis.csv")
    absolute = pd.read_csv(root / "instability" / "absolute_tail_examples.csv")
    profile = pd.read_csv(root / "profile_correlation" / "profile_correlation_summary.csv")
    plt.rcParams.update({
        "font.size": 8.5, "axes.titlesize": 9.5, "axes.labelsize": 8.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "savefig.dpi": 300, "savefig.bbox": "tight",
    })
    fig, axes = plt.subplots(2, 2, figsize=(7.6, 6.0))

    ax = axes[0, 0]
    ax.scatter(released["wtd_adjusted_published"], released["wtd_adjusted"], s=18, color="#4C72B0")
    limit = max(released["wtd_adjusted_published"].max(), released["wtd_adjusted"].max()) + 0.02
    ax.plot([0, limit], [0, limit], color="#333333", linewidth=0.8)
    ax.set(xlabel="Published null-referenced WTD", ylabel="Reanalysis", title="A. Public trials recover the rounded table",
           xlim=(0, limit), ylim=(0, limit))

    ax = axes[0, 1]
    central = released[released["cell"] == "mmlu_pro.gpt54"].iloc[0]
    values = [central["wtd_raw"], central["wtd_adjusted"], central["split_wtd"]]
    ax.bar([0, 1, 2], values, color=["#C44E52", "#4C72B0", "#55A868"])
    ax.set_xticks([0, 1, 2], ["raw", "null-\nreferenced", "held-out\nsplit"])
    ax.set_ylabel("WTD")
    ax.set_title("B. Estimators remain distinct\nMMLU-Pro / gpt-5.4")

    ax = axes[1, 0]
    cases = absolute[absolute["case"].isin(["stable_poor", "sparse_collapse"])]
    x = np.arange(len(cases))
    width = 0.34
    ax.bar(x - width / 2, cases["true_wtd"], width, label="change WTD", color="#C44E52")
    ax.bar(x + width / 2, cases["true_absolute_loss_tail"], width, label="case-risk tail", color="#4C72B0")
    ax.set_xticks(x, cases["case"].str.replace("_", "\n"))
    ax.set_ylabel("Latent value")
    ax.set_title("C. Stable failure requires absolute risk")
    ax.legend(frameon=False, fontsize=8)
    for position, value in zip(x - width / 2, cases["true_wtd"]):
        if np.isclose(value, 0.0):
            ax.text(position, 0.015, "0", ha="center", va="bottom", color="#8B2F33", fontsize=8)

    ax = axes[1, 1]
    selected = profile[profile["scenario"].isin(["moderate_transport", "low_spread"])]
    x = np.arange(len(selected))
    ax.errorbar(x, selected["mean_observed_r"], yerr=selected["sd_observed_r"],
                fmt="o", capsize=3, color="#4C72B0", label="observed mean ± SD")
    ax.scatter(x, selected["true_r"], marker="_", s=180, linewidths=2.0,
               color="#222222", label="latent r")
    ax.set_xticks(x, ["moderate\nspread", "low\nspread"])
    ax.set_ylim(-0.1, 0.8)
    ax.set_ylabel("Profile correlation r")
    ax.set_title("D. Ten-domain profile correlation depends on spread")
    ax.legend(frameon=False, fontsize=8)

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    summary = evidence_summary(args.output_root)
    (args.output_root / "evidence_summary.json").write_text(
        json.dumps(json_safe(summary), indent=2) + "\n"
    )
    table = compact_table(args.output_root)
    table.to_csv(args.output_root / "section5_evidence_table.csv", index=False)
    write_table_tex(table, args.output_root / "section5_evidence_table.tex")
    plot_compact(args.output_root, args.output_root / "section5_evidence.pdf")
    print(f"Wrote compact evidence artifacts to {args.output_root}")


if __name__ == "__main__":
    main()
