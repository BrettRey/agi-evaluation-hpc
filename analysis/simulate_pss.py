"""Ten-domain simulation for Pearson profile correlation."""

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

from .metrics import json_safe, pearson_profile


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "outputs" / "profile_correlation"
N_DOMAINS = 10
SCENARIOS = ("preserved_shift", "moderate_transport", "inverted", "low_spread", "flat_perturbed")


def _correlated_profile(rho: float, *, mean: float, spread: float, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Construct two ten-value vectors with an exact Pearson correlation."""
    x = np.linspace(-1.0, 1.0, N_DOMAINS)
    x -= x.mean()
    x /= np.linalg.norm(x)
    rng = np.random.default_rng(seed)
    z = rng.normal(size=N_DOMAINS)
    z -= z.mean()
    z -= x * np.dot(x, z)
    z /= np.linalg.norm(z)
    y = rho * x + math.sqrt(max(0.0, 1.0 - rho**2)) * z
    # Unit standard deviation makes ``spread`` interpretable on probability scale.
    x /= x.std()
    y /= y.std()
    return mean + spread * x, mean + spread * y


def domain_profiles(name: str, seed: int) -> tuple[np.ndarray, np.ndarray, str]:
    if name == "preserved_shift":
        baseline = np.linspace(0.38, 0.78, N_DOMAINS)
        perturbed = baseline - 0.08
        note = "Shape is perfectly preserved despite an eight-point level loss."
    elif name == "moderate_transport":
        baseline, perturbed = _correlated_profile(0.65, mean=0.58, spread=0.11, seed=seed)
        note = "Profiles have a known moderate latent correlation (r=0.65)."
    elif name == "inverted":
        baseline = np.linspace(0.38, 0.78, N_DOMAINS)
        perturbed = baseline[::-1]
        note = "Domain ordering is reversed (r=-1)."
    elif name == "low_spread":
        baseline, perturbed = _correlated_profile(0.65, mean=0.58, spread=0.012, seed=seed)
        note = "The same latent r=0.65 is difficult to estimate when domains barely differ."
    elif name == "flat_perturbed":
        baseline = np.linspace(0.38, 0.78, N_DOMAINS)
        perturbed = np.full(N_DOMAINS, 0.56)
        note = "The perturbed profile has zero variance, so latent profile correlation is undefined."
    else:
        raise ValueError(f"unknown profile-correlation scenario {name!r}")
    return baseline, perturbed, note


def item_population(
    baseline_profile: np.ndarray,
    perturbed_profile: np.ndarray,
    *,
    items_per_domain: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Create paired item probabilities whose domain means equal the profiles."""
    rng = np.random.default_rng(seed)
    base = np.empty((N_DOMAINS, items_per_domain), dtype=float)
    pert = np.empty_like(base)
    for domain in range(N_DOMAINS):
        shared = rng.uniform(-0.055, 0.055, items_per_domain)
        shared -= shared.mean()
        independent = rng.uniform(-0.055, 0.055, items_per_domain)
        independent -= independent.mean()
        pert_offset = 0.55 * shared + 0.45 * independent
        pert_offset -= pert_offset.mean()
        base[domain] = baseline_profile[domain] + shared
        pert[domain] = perturbed_profile[domain] + pert_offset
    if np.any((base < 0) | (base > 1) | (pert < 0) | (pert > 1)):
        raise RuntimeError("item probabilities escaped [0,1]; adjust scenario spread")
    return base, pert


def observe_population(
    p0: np.ndarray,
    p1: np.ndarray,
    *,
    n_trials: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    shape = (*p0.shape, n_trials)
    baseline = rng.binomial(1, p0[..., None], size=shape).astype(float)
    perturbed = rng.binomial(1, p1[..., None], size=shape).astype(float)
    return baseline, perturbed


def profile_from_trials(values: np.ndarray) -> np.ndarray:
    return np.asarray(values, dtype=float).mean(axis=(1, 2))


def fisher_interval(r: float, *, n_pairs: int = N_DOMAINS, level: float = 0.95) -> tuple[float, float]:
    """Conventional Fisher-z interval, shown only as a fragile comparator."""
    if not math.isfinite(r) or n_pairs <= 3:
        return float("nan"), float("nan")
    # 1.95996 is the 97.5th percentile of the standard normal.
    zcrit = 1.959963984540054
    clipped = float(np.clip(r, -1.0 + 1e-12, 1.0 - 1e-12))
    center = np.arctanh(clipped)
    half = zcrit / math.sqrt(n_pairs - 3)
    return float(np.tanh(center - half)), float(np.tanh(center + half))


def nested_bootstrap_interval(
    baseline: np.ndarray,
    perturbed: np.ndarray,
    *,
    n_boot: int,
    seed: int,
    level: float = 0.95,
) -> tuple[float, float, float]:
    """Paired item-cluster plus within-item trial bootstrap for profile r."""
    if n_boot < 1:
        return float("nan"), float("nan"), 1.0
    domains, items, n_base = baseline.shape
    if domains != N_DOMAINS or perturbed.shape[:2] != (domains, items):
        raise ValueError("expected paired domain-by-item trial arrays")
    n_pert = perturbed.shape[2]
    base_hat = baseline.mean(axis=2)
    pert_hat = perturbed.mean(axis=2)
    rng = np.random.default_rng(seed)
    rs = np.empty(n_boot, dtype=float)
    for boot in range(n_boot):
        b_profile = np.empty(domains)
        p_profile = np.empty(domains)
        for domain in range(domains):
            indices = rng.integers(0, items, items)
            # Conditional binomial draws are equivalent to resampling each
            # selected item's observed Bernoulli trials with replacement.
            b_profile[domain] = rng.binomial(n_base, base_hat[domain, indices]).mean() / n_base
            p_profile[domain] = rng.binomial(n_pert, pert_hat[domain, indices]).mean() / n_pert
        rs[boot] = pearson_profile(b_profile, p_profile)
    finite = rs[np.isfinite(rs)]
    invalid_rate = 1.0 - finite.size / n_boot
    if finite.size < 2:
        return float("nan"), float("nan"), invalid_rate
    alpha = (1.0 - level) / 2.0
    lo, hi = np.quantile(finite, [alpha, 1.0 - alpha])
    return float(lo), float(hi), float(invalid_rate)


def run_primary(
    *,
    items_per_domain: int,
    n_trials: int,
    mc_reps: int,
    n_boot: int,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame, dict, dict]:
    rows: list[dict] = []
    notes: dict[str, str] = {}
    latent_profiles: dict[str, dict] = {}
    for scenario_index, scenario in enumerate(SCENARIOS):
        profile0, profile1, note = domain_profiles(scenario, seed + scenario_index)
        notes[scenario] = note
        p0, p1 = item_population(
            profile0, profile1, items_per_domain=items_per_domain,
            seed=seed + 1000 + scenario_index,
        )
        true0, true1 = p0.mean(axis=1), p1.mean(axis=1)
        true_r = pearson_profile(true0, true1)
        latent_profiles[scenario] = {
            "baseline": true0.tolist(),
            "perturbed": true1.tolist(),
            "true_r": true_r,
        }
        rng = np.random.default_rng(seed + scenario_index * 100_000)
        for rep in range(mc_reps):
            baseline, perturbed = observe_population(p0, p1, n_trials=n_trials, rng=rng)
            observed0 = profile_from_trials(baseline)
            observed1 = profile_from_trials(perturbed)
            observed_r = pearson_profile(observed0, observed1)
            fisher_lo, fisher_hi = fisher_interval(observed_r)
            boot_lo, boot_hi, boot_invalid = nested_bootstrap_interval(
                baseline, perturbed, n_boot=n_boot,
                seed=seed + scenario_index * 1_000_000 + rep,
            )
            rows.append({
                "scenario": scenario,
                "rep": rep,
                "n_domains": N_DOMAINS,
                "items_per_domain": items_per_domain,
                "trials_per_item_condition": n_trials,
                "true_r": true_r,
                "observed_r": observed_r,
                "signed_level_change": float((observed1 - observed0).mean()),
                "fisher_lo": fisher_lo,
                "fisher_hi": fisher_hi,
                "bootstrap_lo": boot_lo,
                "bootstrap_hi": boot_hi,
                "bootstrap_invalid_rate": boot_invalid,
            })
    reps = pd.DataFrame(rows)
    summary_rows = []
    for scenario, frame in reps.groupby("scenario", sort=False):
        true_r = float(frame["true_r"].iloc[0])
        observed = frame["observed_r"].to_numpy(dtype=float)
        finite = observed[np.isfinite(observed)]
        true_defined = math.isfinite(true_r)
        fisher_cover = np.nan
        boot_cover = np.nan
        if true_defined:
            fisher_cover = float(np.mean((frame["fisher_lo"] <= true_r) & (true_r <= frame["fisher_hi"])))
            boot_cover = float(np.mean((frame["bootstrap_lo"] <= true_r) & (true_r <= frame["bootstrap_hi"])))
        summary_rows.append({
            "scenario": scenario,
            "n_domains": N_DOMAINS,
            "items_per_domain": items_per_domain,
            "trials_per_item_condition": n_trials,
            "mc_reps": mc_reps,
            "bootstrap_reps": n_boot,
            "true_r": true_r,
            "mean_observed_r": float(finite.mean()) if finite.size else float("nan"),
            "bias_observed_r": float(finite.mean() - true_r) if finite.size and true_defined else float("nan"),
            "rmse_observed_r": float(np.sqrt(np.mean((finite - true_r) ** 2))) if finite.size and true_defined else float("nan"),
            "sd_observed_r": float(finite.std(ddof=1)) if finite.size > 1 else float("nan"),
            "undefined_rate": float(1.0 - finite.size / len(frame)),
            "fisher_coverage": fisher_cover,
            "fisher_mean_width": float((frame["fisher_hi"] - frame["fisher_lo"]).mean()),
            "nested_bootstrap_coverage": boot_cover,
            "nested_bootstrap_mean_width": float((frame["bootstrap_hi"] - frame["bootstrap_lo"]).mean()),
            "bootstrap_invalid_rate": float(frame["bootstrap_invalid_rate"].mean()),
        })
    return reps, pd.DataFrame(summary_rows), notes, latent_profiles


def run_sensitivity(
    *,
    items_grid: list[int],
    trials_grid: list[int],
    mc_reps: int,
    seed: int,
) -> pd.DataFrame:
    rows = []
    for scenario_index, scenario in enumerate(("moderate_transport", "low_spread")):
        profile0, profile1, _ = domain_profiles(scenario, seed + scenario_index)
        for items in items_grid:
            p0, p1 = item_population(
                profile0, profile1, items_per_domain=items,
                seed=seed + 10_000 + scenario_index * 1000 + items,
            )
            true_r = pearson_profile(p0.mean(axis=1), p1.mean(axis=1))
            for trials in trials_grid:
                rng = np.random.default_rng(seed + scenario_index * 1_000_000 + items * 1000 + trials)
                estimates = []
                for _ in range(mc_reps):
                    baseline, perturbed = observe_population(p0, p1, n_trials=trials, rng=rng)
                    estimates.append(pearson_profile(profile_from_trials(baseline), profile_from_trials(perturbed)))
                est = np.asarray(estimates)
                finite = est[np.isfinite(est)]
                rows.append({
                    "scenario": scenario,
                    "n_domains": N_DOMAINS,
                    "items_per_domain": items,
                    "trials_per_item_condition": trials,
                    "mc_reps": mc_reps,
                    "true_r": true_r,
                    "mean_observed_r": float(finite.mean()) if finite.size else float("nan"),
                    "bias": float(finite.mean() - true_r) if finite.size else float("nan"),
                    "rmse": float(np.sqrt(np.mean((finite - true_r) ** 2))) if finite.size else float("nan"),
                    "undefined_rate": float(1.0 - finite.size / est.size),
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


def plot_distributions(reps: pd.DataFrame, path: Path) -> None:
    _style()
    scenarios = list(SCENARIOS)
    data = [reps.loc[reps["scenario"] == scenario, "observed_r"].dropna().to_numpy() for scenario in scenarios]
    fig, ax = plt.subplots(figsize=(8.0, 3.8))
    parts = ax.violinplot(data, positions=np.arange(len(scenarios)), showmeans=False, showextrema=False)
    for body in parts["bodies"]:
        body.set_facecolor("#4C72B0")
        body.set_alpha(0.45)
    for i, scenario in enumerate(scenarios):
        values = data[i]
        if values.size:
            ax.scatter(i, np.median(values), color="#4C72B0", s=16, zorder=3)
        truth = reps.loc[reps["scenario"] == scenario, "true_r"].iloc[0]
        if math.isfinite(float(truth)):
            ax.scatter(i, truth, color="#222222", marker="_", s=180, linewidths=2.2, zorder=4)
    ax.axhline(0, color="#888888", linewidth=0.7)
    ax.set_ylim(-1.05, 1.05)
    ax.set_ylabel("Profile correlation r")
    ax.set_xticks(np.arange(len(scenarios)), [x.replace("_", "\n") for x in scenarios])
    ax.set_title("Profile-correlation uncertainty with only ten domain means")
    ax.text(0.99, 0.03, "black bar: latent r; dot: observed median", transform=ax.transAxes,
            ha="right", va="bottom", color="#555555")
    fig.savefig(path)
    plt.close(fig)


def plot_sensitivity(frame: pd.DataFrame, path: Path) -> None:
    _style()
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.5), sharey=True)
    for ax, scenario in zip(axes, ("moderate_transport", "low_spread")):
        subset = frame[frame["scenario"] == scenario]
        for items, group in subset.groupby("items_per_domain"):
            group = group.sort_values("trials_per_item_condition")
            ax.plot(group["trials_per_item_condition"], group["rmse"], marker="o", label=f"{items} items/domain")
        ax.set_xscale("log")
        ax.set_xticks(sorted(subset["trials_per_item_condition"].unique()))
        ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        ax.set_xlabel("Trials per item and condition")
        ax.set_title(scenario.replace("_", " "))
    axes[0].set_ylabel("RMSE of profile correlation")
    axes[1].legend(frameon=False)
    fig.suptitle("Ten domains: trial count can't replace profile spread", y=1.02)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_profiles(latent_profiles: dict, path: Path) -> None:
    _style()
    fig, axes = plt.subplots(1, 3, figsize=(9.3, 3.0), sharey=True)
    for ax, scenario in zip(axes, ("preserved_shift", "moderate_transport", "flat_perturbed")):
        profile = latent_profiles[scenario]
        domains = np.arange(1, N_DOMAINS + 1)
        ax.plot(domains, profile["baseline"], marker="o", label="baseline", color="#4C72B0")
        ax.plot(domains, profile["perturbed"], marker="o", label="perturbed", color="#C44E52")
        r = profile["true_r"]
        title_r = "undefined" if not math.isfinite(r) else f"r={r:.2f}"
        ax.set_title(f"{scenario.replace('_', ' ')}\n{title_r}")
        ax.set_xlabel("Domain")
        ax.set_xticks([1, 5, 10])
    axes[0].set_ylabel("Latent domain mean")
    axes[-1].legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def write_latex_table(summary: pd.DataFrame, path: Path) -> None:
    lines = [
        "% Generated by python -m analysis.simulate_pss; do not edit by hand.",
        "\\begin{tabular}{lrrrrr}",
        "\\toprule",
        "Scenario & True $r$ & Mean $\\hat r$ & RMSE & Undefined & Bootstrap coverage \\\\",
        "\\midrule",
    ]
    for row in summary.itertuples(index=False):
        def fmt(value: float) -> str:
            if not math.isfinite(float(value)):
                return "--"
            clean = 0.0 if abs(float(value)) < 0.005 else float(value)
            return f"{clean:.2f}"
        scenario = row.scenario.replace("_", " ")
        lines.append(
            f"{scenario} & {fmt(row.true_r)} & {fmt(row.mean_observed_r)} & "
            f"{fmt(row.rmse_observed_r)} & {row.undefined_rate:.2f} & "
            f"{fmt(row.nested_bootstrap_coverage)} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}", ""])
    path.write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("smoke", "standard"), default="standard")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=20260717)
    args = parser.parse_args()
    config = {
        "smoke": {"items_per_domain": 12, "n_trials": 5, "mc_reps": 4, "n_boot": 8,
                  "items_grid": [10, 20], "trials_grid": [2, 10], "sensitivity_mc": 5},
        "standard": {"items_per_domain": 50, "n_trials": 20, "mc_reps": 240, "n_boot": 160,
                     "items_grid": [20, 50, 100], "trials_grid": [2, 5, 10, 20, 50],
                     "sensitivity_mc": 160},
    }[args.profile]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    primary_args = {key: config[key] for key in ("items_per_domain", "n_trials", "mc_reps", "n_boot")}
    reps, summary, notes, latent_profiles = run_primary(seed=args.seed, **primary_args)
    sensitivity = run_sensitivity(
        items_grid=config["items_grid"], trials_grid=config["trials_grid"],
        mc_reps=config["sensitivity_mc"], seed=args.seed + 9_000_000,
    )
    reps.to_csv(args.output_dir / "profile_correlation_replicates.csv", index=False)
    summary.to_csv(args.output_dir / "profile_correlation_summary.csv", index=False)
    sensitivity.to_csv(args.output_dir / "profile_correlation_sensitivity.csv", index=False)
    write_latex_table(summary, args.output_dir / "profile_correlation_summary.tex")
    metadata = {
        "profile": args.profile,
        "seed": args.seed,
        "config": config,
        "n_domains": N_DOMAINS,
        "scenario_notes": notes,
        "latent_profiles": latent_profiles,
        "limitations": [
            "The simulation tests estimation with ten domain means; it doesn't validate CHC domains for machines.",
            "The Fisher interval treats ten domain pairs as exact iid observations and is included only as a comparator.",
            "The nested bootstrap preserves paired items and resamples items and within-item trials; it doesn't establish transport to new model families."
        ],
    }
    (args.output_dir / "run_metadata.json").write_text(json.dumps(json_safe(metadata), indent=2) + "\n")
    plot_distributions(reps, args.output_dir / "profile_correlation_distributions.pdf")
    plot_sensitivity(sensitivity, args.output_dir / "profile_correlation_sensitivity.pdf")
    plot_profiles(latent_profiles, args.output_dir / "profile_correlation_profiles.pdf")
    print(f"Wrote profile-correlation simulation outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
