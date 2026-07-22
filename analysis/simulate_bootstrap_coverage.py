"""Known-truth calibration check for the item bootstrap.

The item bootstrap resamples items inside a fixed design. This module asks what
its intervals actually cover. Three estimands are separated:

``population_signed_delta``
    the population mean paired change;
``population_raw_wtd``
    the value the raw worst-tail statistic takes on the population at the same
    per-item trial count, so response-selection inflation is included;
``population_latent_wtd``
    the worst-tail mean of the latent per-item degradations, with no response
    noise.

The first two are what the bootstrap estimates. The third is what a reader may
assume a tail interval refers to, and the interval does not cover it: selection
on response noise shifts the statistic by far more than item resampling varies
it. Reporting that gap is the point of this check.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .metrics import basic_metrics, item_bootstrap, json_safe, upper_tail_mean


HERE = Path(__file__).resolve().parent

PROFILES = {
    "smoke": {"reps": 40, "n_boot": 200, "population": 40_000},
    "standard": {"reps": 400, "n_boot": 400, "population": 400_000},
}


def draw_latents(n: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Latent baseline and perturbed item probabilities.

    Baselines are skewed high, matching benchmark accuracies in the released
    design. Effects are heterogeneous with a small negative mean, so the
    aggregate barely moves while individual items move in both directions.
    """
    baseline = rng.beta(6.0, 2.0, size=n)
    effect = rng.normal(-0.02, 0.08, size=n)
    return baseline, np.clip(baseline + effect, 0.0, 1.0)


def population_truths(
    *, population: int, n_trials: int, q: float, seed: int
) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    baseline, perturbed = draw_latents(population, rng)
    base_hat = rng.binomial(n_trials, baseline) / n_trials
    pert_hat = rng.binomial(n_trials, perturbed) / n_trials
    return {
        "population_signed_delta": float((perturbed - baseline).mean()),
        "population_ins_raw": float(np.abs(base_hat - pert_hat).mean()),
        "population_latent_wtd": upper_tail_mean(baseline - perturbed, q),
        "population_raw_wtd": upper_tail_mean(base_hat - pert_hat, q),
    }


def run(
    *, reps: int, n_items: int, n_trials: int, q: float, n_boot: int, population: int, seed: int
) -> tuple[pd.DataFrame, dict[str, float]]:
    truths = population_truths(population=population, n_trials=n_trials, q=q, seed=seed)
    rng = np.random.default_rng(seed + 1)
    rows = []
    for rep in range(reps):
        baseline_p, perturbed_p = draw_latents(n_items, rng)
        baseline = rng.binomial(1, np.repeat(baseline_p[:, None], n_trials, axis=1)).astype(float)
        perturbed = rng.binomial(1, np.repeat(perturbed_p[:, None], n_trials, axis=1)).astype(float)
        point = basic_metrics(baseline, perturbed, q=q)
        boot = item_bootstrap(
            baseline, perturbed, q=q, n_boot=n_boot, seed=int(rng.integers(1_000_000))
        )
        rows.append(
            {
                "rep": rep,
                "signed_delta": point["signed_delta"],
                "ins_raw": point["ins_raw"],
                "wtd_raw": point["wtd_raw"],
                "signed_covers_population": bool(
                    boot["signed_delta_boot_lo"]
                    <= truths["population_signed_delta"]
                    <= boot["signed_delta_boot_hi"]
                ),
                "ins_covers_population": bool(
                    boot["ins_raw_boot_lo"]
                    <= truths["population_ins_raw"]
                    <= boot["ins_raw_boot_hi"]
                ),
                "wtd_covers_population_raw": bool(
                    boot["wtd_raw_boot_lo"]
                    <= truths["population_raw_wtd"]
                    <= boot["wtd_raw_boot_hi"]
                ),
                "wtd_covers_latent": bool(
                    boot["wtd_raw_boot_lo"]
                    <= truths["population_latent_wtd"]
                    <= boot["wtd_raw_boot_hi"]
                ),
                "signed_width": boot["signed_delta_boot_hi"] - boot["signed_delta_boot_lo"],
                "wtd_width": boot["wtd_raw_boot_hi"] - boot["wtd_raw_boot_lo"],
            }
        )
    return pd.DataFrame(rows), truths


def summarize(frame: pd.DataFrame, truths: dict[str, float]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "quantity": "signed_delta",
                "estimand": "population signed change",
                "truth": truths["population_signed_delta"],
                "mean_estimate": frame["signed_delta"].mean(),
                "coverage": frame["signed_covers_population"].mean(),
                "mean_width": frame["signed_width"].mean(),
            },
            {
                "quantity": "ins_raw",
                "estimand": "population INS at this trial count",
                "truth": truths["population_ins_raw"],
                "mean_estimate": frame["ins_raw"].mean(),
                "coverage": frame["ins_covers_population"].mean(),
                "mean_width": float("nan"),
            },
            {
                "quantity": "wtd_raw",
                "estimand": "population raw WTD at this trial count",
                "truth": truths["population_raw_wtd"],
                "mean_estimate": frame["wtd_raw"].mean(),
                "coverage": frame["wtd_covers_population_raw"].mean(),
                "mean_width": frame["wtd_width"].mean(),
            },
            {
                "quantity": "wtd_raw",
                "estimand": "population LATENT WTD",
                "truth": truths["population_latent_wtd"],
                "mean_estimate": frame["wtd_raw"].mean(),
                "coverage": frame["wtd_covers_latent"].mean(),
                "mean_width": frame["wtd_width"].mean(),
            },
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=tuple(PROFILES), default="standard")
    parser.add_argument("--n-items", type=int, default=500)
    parser.add_argument("--n-trials", type=int, default=20)
    parser.add_argument("--tail-q", type=float, default=0.10)
    parser.add_argument("--seed", type=int, default=20260722)
    parser.add_argument("--output-dir", type=Path, default=HERE / "outputs" / "bootstrap_coverage")
    args = parser.parse_args()

    config = PROFILES[args.profile]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    frame, truths = run(
        reps=config["reps"],
        n_items=args.n_items,
        n_trials=args.n_trials,
        q=args.tail_q,
        n_boot=config["n_boot"],
        population=config["population"],
        seed=args.seed,
    )
    summary = summarize(frame, truths)
    frame.to_csv(args.output_dir / "coverage_replicates.csv", index=False)
    summary.to_csv(args.output_dir / "coverage_summary.csv", index=False)
    metadata = {
        "profile": args.profile,
        "n_items": args.n_items,
        "n_trials": args.n_trials,
        "tail_q": args.tail_q,
        "seed": args.seed,
        **config,
        **truths,
        "noise_inflation_raw_minus_latent": truths["population_raw_wtd"]
        - truths["population_latent_wtd"],
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(json_safe(metadata), indent=2) + "\n"
    )
    print(summary.to_string(index=False))
    print(f"\nWrote bootstrap coverage check to {args.output_dir}")


if __name__ == "__main__":
    main()
