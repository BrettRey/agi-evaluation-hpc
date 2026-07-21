"""Known-truth simulations for cancellation, INS/WTD, and case-risk tails."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .metrics import (
    adjusted_metrics,
    basic_metrics,
    crossfit_absolute_loss_tail,
    json_safe,
    split_sample_wtd,
    upper_tail_mean,
)


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "outputs" / "instability"
SCENARIOS = ("null_effect", "diffuse", "symmetric_churn", "sparse_collapse", "floor", "ceiling")

PALETTE = {
    "truth": "#222222",
    "raw": "#C44E52",
    "adjusted": "#4C72B0",
    "split": "#55A868",
}


def latent_scenario(name: str, n_items: int, seed: int) -> tuple[np.ndarray, np.ndarray, str]:
    """Construct fixed item-level probabilities for a named known-truth case."""
    if name not in SCENARIOS:
        raise ValueError(f"unknown scenario {name!r}")
    rng = np.random.default_rng(seed)
    if name == "null_effect":
        p0 = rng.uniform(0.25, 0.90, n_items)
        p1 = p0.copy()
        note = "No latent condition effect; positive raw INS/WTD is sampling and selection noise."
    elif name == "diffuse":
        p0 = rng.uniform(0.35, 0.90, n_items)
        p1 = np.clip(p0 - 0.08, 0.0, 1.0)
        note = "Every item suffers the same 8-point degradation."
    elif name == "symmetric_churn":
        p0 = rng.uniform(0.30, 0.70, n_items)
        direction = np.ones(n_items)
        direction[: n_items // 2] = -1.0
        rng.shuffle(direction)
        p1 = p0 + 0.15 * direction
        note = "Equal 15-point gains and losses cancel in the mean while INS remains positive."
    elif name == "sparse_collapse":
        p0 = rng.uniform(0.72, 0.92, n_items)
        p1 = p0.copy()
        harmed = rng.choice(n_items, size=max(1, int(round(0.10 * n_items))), replace=False)
        p1[harmed] = np.clip(p1[harmed] - 0.55, 0.0, 1.0)
        note = "Ten percent of items collapse by 55 points; the rest are unchanged."
    elif name == "floor":
        p0 = rng.uniform(0.02, 0.12, n_items)
        p1 = p0.copy()
        harmed = rng.choice(n_items, size=max(1, int(round(0.25 * n_items))), replace=False)
        p1[harmed] = np.clip(p1[harmed] - 0.08, 0.0, 1.0)
        note = "Low baseline accuracy compresses possible degradation and makes stability ambiguous."
    else:  # ceiling
        p0 = rng.uniform(0.88, 0.98, n_items)
        order = rng.permutation(n_items)
        p1 = p0.copy()
        quarter = n_items // 4
        p1[order[:quarter]] = np.clip(p1[order[:quarter]] + 0.08, 0.0, 1.0)
        p1[order[quarter : 2 * quarter]] = np.clip(p1[order[quarter : 2 * quarter]] - 0.08, 0.0, 1.0)
        note = "Nominally balanced gains/losses are asymmetrically compressed at the ceiling."
    return p0, p1, note


def truth_metrics(p0: np.ndarray, p1: np.ndarray, q: float) -> dict[str, float]:
    point = basic_metrics(p0[:, None], p1[:, None], q=q)
    return {
        "signed_delta": float(point["signed_delta"]),
        "ins": float(point["ins_raw"]),
        "wtd": float(point["wtd_raw"]),
        "absolute_loss_tail": float(point["absolute_loss_tail_raw"]),
    }


def one_replication(
    p0: np.ndarray,
    p1: np.ndarray,
    *,
    n_trials: int,
    q: float,
    null_boot: int,
    split_reps: int,
    seed: int,
) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    baseline = rng.binomial(1, p0[:, None], size=(p0.size, n_trials)).astype(float)
    perturbed = rng.binomial(1, p1[:, None], size=(p1.size, n_trials)).astype(float)
    adjusted = adjusted_metrics(
        baseline,
        perturbed,
        q=q,
        n_boot=null_boot,
        seed=seed + 1,
    )
    split = split_sample_wtd(
        baseline,
        perturbed,
        q=q,
        n_reps=split_reps,
        seed=seed + 2,
        true_degradation=p0 - p1,
    )
    return {
        "signed_delta": float(adjusted["signed_delta"]),
        "ins_raw": float(adjusted["ins_raw"]),
        "ins_adjusted": float(adjusted["ins_adjusted"]),
        "ins_floor": float(adjusted["ins_floor"]),
        "wtd_raw": float(adjusted["wtd_raw"]),
        "wtd_adjusted": float(adjusted["wtd_adjusted"]),
        "wtd_floor": float(adjusted["wtd_floor"]),
        "wtd_split": float(split["split_wtd"]),
        "wtd_selected_truth": float(split["selected_set_truth"]),
        "wtd_oracle_truth": float(split["oracle_tail_truth"]),
    }


def summarize_estimates(records: pd.DataFrame, truth: dict[str, float]) -> list[dict]:
    specs = [
        ("signed_delta", "signed", truth["signed_delta"]),
        ("ins_raw", "raw", truth["ins"]),
        ("ins_adjusted", "adjusted", truth["ins"]),
        ("wtd_raw", "raw", truth["wtd"]),
        ("wtd_adjusted", "adjusted", truth["wtd"]),
        ("wtd_split", "split_oracle_comparison", truth["wtd"]),
    ]
    rows: list[dict] = []
    for metric, estimator, target in specs:
        values = records[metric].to_numpy(dtype=float)
        error = values - target
        rows.append({
            "metric": metric.split("_")[0],
            "estimator": estimator,
            "estimand": "oracle_tail" if metric.startswith("wtd") else "latent_metric",
            "truth": target,
            "estimate_mean": float(values.mean()),
            "bias": float(error.mean()),
            "rmse": float(np.sqrt(np.mean(error**2))),
            "estimate_sd": float(values.std(ddof=1)) if values.size > 1 else float("nan"),
            "negative_rate": float(np.mean(values < 0.0)),
        })
    split_error = records["wtd_split"].to_numpy() - records["wtd_selected_truth"].to_numpy()
    rows.append({
        "metric": "wtd",
        "estimator": "split",
        "estimand": "noisy_selected_set",
        "truth": float(records["wtd_selected_truth"].mean()),
        "estimate_mean": float(records["wtd_split"].mean()),
        "bias": float(split_error.mean()),
        "rmse": float(np.sqrt(np.mean(split_error**2))),
        "estimate_sd": float(records["wtd_split"].std(ddof=1)) if len(records) > 1 else float("nan"),
        "negative_rate": float(np.mean(records["wtd_split"] < 0.0)),
    })
    return rows


def run_grid(
    *,
    n_items: int,
    mc_reps: int,
    null_boot: int,
    split_reps: int,
    trial_counts: list[int],
    tail_qs: list[float],
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    primary_rows: list[dict] = []
    sensitivity_rows: list[dict] = []
    scenario_notes: dict[str, str] = {}
    primary_trials, primary_q = 20, 0.10
    for scenario_index, scenario in enumerate(SCENARIOS):
        p0, p1, note = latent_scenario(scenario, n_items, seed + 1000 * scenario_index)
        scenario_notes[scenario] = note
        truth = truth_metrics(p0, p1, primary_q)
        rep_rows = []
        for rep in range(mc_reps):
            row = one_replication(
                p0,
                p1,
                n_trials=primary_trials,
                q=primary_q,
                null_boot=null_boot,
                split_reps=split_reps,
                seed=seed + scenario_index * 100_000 + rep * 17,
            )
            rep_rows.append(row)
        summarized = summarize_estimates(pd.DataFrame(rep_rows), truth)
        for row in summarized:
            primary_rows.append({
                "scenario": scenario,
                "n_items": n_items,
                "n_trials": primary_trials,
                "tail_q": primary_q,
                "mc_reps": mc_reps,
                **row,
            })

        sensitivity_mc = max(4, mc_reps // 3)
        sensitivity_boot = max(8, null_boot // 2)
        sensitivity_split = max(8, split_reps // 2)
        for n_trials in trial_counts:
            for q in tail_qs:
                truth = truth_metrics(p0, p1, q)
                reps = []
                for rep in range(sensitivity_mc):
                    reps.append(one_replication(
                        p0,
                        p1,
                        n_trials=n_trials,
                        q=q,
                        null_boot=sensitivity_boot,
                        split_reps=sensitivity_split,
                        seed=(seed + 10_000_000 + scenario_index * 100_000
                              + n_trials * 1000 + int(q * 100) * 100 + rep),
                    ))
                for row in summarize_estimates(pd.DataFrame(reps), truth):
                    sensitivity_rows.append({
                        "scenario": scenario,
                        "n_items": n_items,
                        "n_trials": n_trials,
                        "tail_q": q,
                        "mc_reps": sensitivity_mc,
                        **row,
                    })
    return pd.DataFrame(primary_rows), pd.DataFrame(sensitivity_rows), scenario_notes


def cancellation_example(n_items: int = 100) -> pd.DataFrame:
    p0 = np.full(n_items, 0.60)
    delta = np.full(n_items, 0.20)
    delta[: n_items // 2] = -0.20
    return pd.DataFrame({
        "item": np.arange(1, n_items + 1),
        "baseline_probability": p0,
        "perturbed_probability": p0 + delta,
        "delta": delta,
        "degradation": -delta,
    })


def absolute_tail_examples(*, n_items: int, n_trials: int, q: float, split_reps: int, seed: int) -> pd.DataFrame:
    cases = {
        "stable_poor": (np.full(n_items, 0.20), np.full(n_items, 0.20)),
        "stable_strong": (np.full(n_items, 0.90), np.full(n_items, 0.90)),
        "uniform_degradation": (np.full(n_items, 0.80), np.full(n_items, 0.60)),
        "sparse_collapse": (
            np.full(n_items, 0.90),
            np.concatenate([np.full(max(1, int(round(q * n_items))), 0.20),
                            np.full(n_items - max(1, int(round(q * n_items))), 0.90)]),
        ),
    }
    rows = []
    rng = np.random.default_rng(seed)
    for index, (name, (p0, p1)) in enumerate(cases.items()):
        baseline = rng.binomial(1, p0[:, None], size=(n_items, n_trials)).astype(float)
        perturbed = rng.binomial(1, p1[:, None], size=(n_items, n_trials)).astype(float)
        point = basic_metrics(baseline, perturbed, q=q)
        split = split_sample_wtd(
            baseline, perturbed, q=q, n_reps=split_reps,
            seed=seed + 100 + index, true_degradation=p0 - p1,
        )
        absolute = crossfit_absolute_loss_tail(
            perturbed, q=q, n_reps=split_reps,
            seed=seed + 200 + index, true_loss=1.0 - p1,
        )
        rows.append({
            "case": name,
            "true_mean_degradation": float(np.mean(p0 - p1)),
            "true_wtd": upper_tail_mean(p0 - p1, q),
            "true_absolute_loss_tail": upper_tail_mean(1.0 - p1, q),
            "observed_wtd_raw": float(point["wtd_raw"]),
            "observed_wtd_split": float(split["split_wtd"]),
            "observed_absolute_loss_tail_raw": float(absolute["absolute_loss_tail_raw"]),
            "observed_absolute_loss_tail_crossfit": float(absolute["absolute_loss_tail_crossfit"]),
        })
    return pd.DataFrame(rows)


def _style() -> None:
    plt.rcParams.update({
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.dpi": 160,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })


def plot_cancellation(frame: pd.DataFrame, path: Path) -> None:
    _style()
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    colors = np.where(frame["delta"] < 0, "#C44E52", "#4C72B0")
    ax.bar(frame["item"], frame["delta"], color=colors, width=1.0, linewidth=0)
    ax.axhline(0, color="#333333", linewidth=0.8)
    ax.set(xlabel="Item", ylabel="Perturbed minus baseline", title="Mean change cancels while item-level instability remains")
    ax.text(0.99, 0.95, "signed mean = 0.00\nINS = 0.20\nworst-10% degradation = 0.20",
            transform=ax.transAxes, ha="right", va="top")
    fig.savefig(path)
    plt.close(fig)


def plot_primary(summary: pd.DataFrame, path: Path) -> None:
    _style()
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.8), sharex=True)
    scenarios = list(SCENARIOS)
    specs = [
        (axes[0], "ins", [("raw", "raw"), ("adjusted", "adjusted")], "INS"),
        (axes[1], "wtd", [("raw", "raw"), ("adjusted", "adjusted"),
                          ("split_oracle_comparison", "split")], "Worst-tail degradation"),
    ]
    x = np.arange(len(scenarios))
    for ax, metric, estimators, title in specs:
        subset = summary[(summary["metric"] == metric) & (summary["estimand"] != "noisy_selected_set")]
        width = 0.70 / len(estimators)
        for i, (estimator, label) in enumerate(estimators):
            values = []
            for scenario in scenarios:
                match = subset[(subset["scenario"] == scenario) & (subset["estimator"] == estimator)]
                values.append(float(match["estimate_mean"].iloc[0]))
            ax.bar(x + (i - (len(estimators) - 1) / 2) * width, values, width,
                   label="null-referenced" if label == "adjusted" else label,
                   color=PALETTE[label], alpha=0.88)
        truth = []
        for scenario in scenarios:
            match = subset[subset["scenario"] == scenario]
            truth.append(float(match["truth"].iloc[0]))
        ax.scatter(x, truth, marker="_", s=170, linewidths=2.0, color=PALETTE["truth"], label="latent truth")
        ax.axhline(0, color="#777777", linewidth=0.7)
        ax.set_title(title)
        labels = {
            "null_effect": "null\neffect", "diffuse": "diffuse",
            "symmetric_churn": "symmetric\nchurn", "sparse_collapse": "sparse\ncollapse",
            "floor": "floor", "ceiling": "ceiling",
        }
        ax.set_xticks(x, [labels[s] for s in scenarios], rotation=0)
        ax.tick_params(axis="x", labelsize=8)
        ax.set_ylabel("Probability scale")
    handles, labels = axes[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=4, frameon=False)
    fig.subplots_adjust(top=0.78, wspace=0.25)
    fig.savefig(path)
    plt.close(fig)


def plot_sensitivity(summary: pd.DataFrame, path: Path) -> None:
    _style()
    subset = summary[(summary["scenario"] == "sparse_collapse")
                     & (summary["metric"] == "wtd")
                     & (summary["estimator"].isin(["raw", "adjusted", "split_oracle_comparison"]))
                     & (summary["estimand"] == "oracle_tail")]
    qs = sorted(subset["tail_q"].unique())
    fig, axes = plt.subplots(1, len(qs), figsize=(10.0, 3.2), sharey=True)
    labels = [("raw", "raw"), ("adjusted", "adjusted"), ("split_oracle_comparison", "split")]
    for ax, q in zip(np.atleast_1d(axes), qs):
        qset = subset[subset["tail_q"] == q]
        for estimator, label in labels:
            rows = qset[qset["estimator"] == estimator].sort_values("n_trials")
            ax.plot(
                rows["n_trials"],
                rows["bias"],
                marker="o",
                label="null-referenced" if label == "adjusted" else label,
                color=PALETTE[label],
            )
        ax.axhline(0, color="#333333", linewidth=0.8)
        ax.set_xscale("log")
        ax.set_xticks(sorted(qset["n_trials"].unique()))
        ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        ax.set_title(f"tail q = {q:.0%}")
        ax.set_xlabel("Trials per condition")
    axes[0].set_ylabel("Bias relative to oracle tail")
    handles, labels_out = axes[-1].get_legend_handles_labels()
    fig.legend(handles, labels_out, loc="upper center", ncol=3, frameon=False)
    fig.suptitle("Sparse-collapse WTD sensitivity", y=1.02)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_absolute_tail(frame: pd.DataFrame, path: Path) -> None:
    _style()
    x = np.arange(len(frame))
    width = 0.34
    fig, ax = plt.subplots(figsize=(7.4, 3.5))
    ax.bar(x - width / 2, frame["true_wtd"], width, label="true WTD (change)", color="#C44E52")
    ax.bar(x + width / 2, frame["true_absolute_loss_tail"], width,
           label="true case-risk tail", color="#4C72B0")
    ax.set_xticks(x, frame["case"].str.replace("_", "\n"))
    ax.set_ylabel("Probability scale")
    ax.set_title("Change-based WTD doesn't measure stable case risk")
    ax.legend(frameon=False, ncol=2, loc="upper center")
    fig.savefig(path)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("smoke", "standard"), default="standard")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=20260717)
    args = parser.parse_args()
    config = {
        "smoke": {"n_items": 80, "mc_reps": 3, "null_boot": 8, "split_reps": 8,
                  "trial_counts": [2, 10, 20], "tail_qs": [0.10, 0.20]},
        "standard": {"n_items": 300, "mc_reps": 36, "null_boot": 48, "split_reps": 48,
                     "trial_counts": [2, 5, 10, 20, 50], "tail_qs": [0.05, 0.10, 0.20]},
    }[args.profile]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    primary, sensitivity, notes = run_grid(seed=args.seed, **config)
    cancellation = cancellation_example()
    absolute = absolute_tail_examples(
        n_items=config["n_items"], n_trials=20, q=0.10,
        split_reps=config["split_reps"], seed=args.seed + 999,
    )
    primary.to_csv(args.output_dir / "known_truth_summary.csv", index=False)
    sensitivity.to_csv(args.output_dir / "trial_tail_sensitivity.csv", index=False)
    cancellation.to_csv(args.output_dir / "cancellation_items.csv", index=False)
    absolute.to_csv(args.output_dir / "absolute_tail_examples.csv", index=False)
    metadata = {
        "profile": args.profile,
        "seed": args.seed,
        "config": config,
        "scenario_notes": notes,
        "interpretation": {
            "baseline_floor": "Null-referenced diagnostic: raw minus the estimated baseline-only pseudo-null expectation; untruncated.",
            "split_tail": "Unbiased for the noisy-selected set, not necessarily the oracle latent tail.",
            "absolute_tail": "Perturbed-condition loss, separate from condition-to-condition WTD."
        },
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(json_safe(metadata), indent=2) + "\n"
    )
    plot_cancellation(cancellation, args.output_dir / "cancellation.pdf")
    plot_primary(primary, args.output_dir / "estimator_comparison.pdf")
    plot_sensitivity(sensitivity, args.output_dir / "wtd_sensitivity.pdf")
    plot_absolute_tail(absolute, args.output_dir / "absolute_tail.pdf")
    print(f"Wrote instability simulation outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
