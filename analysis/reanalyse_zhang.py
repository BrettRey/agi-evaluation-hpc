"""Reanalyse all 32 released Zhang et al. model-by-benchmark cells.

This script downloads only immutable, checksummed Parquet snapshots named in
``source_manifest.lock.json``. It never calls a model or grading API.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import urllib.request

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .metrics import (
    adjusted_metrics,
    crossfit_absolute_loss_tail,
    directional_components,
    item_bootstrap,
    json_safe,
    split_half_reliability,
    split_sample_wtd,
)


HERE = Path(__file__).resolve().parent
DEFAULT_LOCK = HERE / "source_manifest.lock.json"
DEFAULT_CACHE = HERE / "cache"
DEFAULT_OUTPUT = HERE / "outputs" / "zhang_reanalysis"
PUBLISHED = HERE / "published_main_results.csv"


def stable_seed(label: str, base: int) -> int:
    digest = hashlib.sha256(label.encode("utf-8")).digest()
    return (base + int.from_bytes(digest[:4], "big")) % (2**32 - 1)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch_dataset(
    repo: str,
    lock: dict,
    *,
    cache_dir: Path,
    offline: bool,
) -> tuple[list[Path], list[dict]]:
    """Materialize a locked dataset and verify every available LFS SHA-256."""
    source = lock["datasets"][repo]
    local_root = cache_dir / repo.replace("/", "--") / source["revision"]
    paths: list[Path] = []
    audit: list[dict] = []
    for file_info in source["parquet"]:
        local = local_root / file_info["path"]
        expected = file_info.get("lfs_sha256")
        status = "cached"
        actual = sha256_file(local) if local.exists() else None
        if not local.exists() or (expected and actual != expected):
            if offline:
                reason = "missing" if not local.exists() else "checksum mismatch"
                raise FileNotFoundError(f"Offline cache {reason}: {local}")
            local.parent.mkdir(parents=True, exist_ok=True)
            temporary = local.with_suffix(local.suffix + ".part")
            request = urllib.request.Request(
                file_info["download_url"], headers={"User-Agent": "agi-evaluation-repro/1"}
            )
            with urllib.request.urlopen(request, timeout=180) as response, temporary.open("wb") as out:
                shutil.copyfileobj(response, out, length=1024 * 1024)
            actual = sha256_file(temporary)
            if expected and actual != expected:
                temporary.unlink(missing_ok=True)
                raise RuntimeError(
                    f"Checksum mismatch for {repo}/{file_info['path']}: {actual} != {expected}"
                )
            temporary.replace(local)
            status = "downloaded"
        paths.append(local)
        audit.append({
            "repo": repo,
            "revision": source["revision"],
            "parquet_path": file_info["path"],
            "bytes": local.stat().st_size,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "verified": bool(not expected or actual == expected),
            "status": status,
            "local_path": str(local.relative_to(cache_dir)),
        })
    return paths, audit


def read_trials(paths: list[Path]) -> pd.DataFrame:
    frames = []
    for path in paths:
        try:
            frame = pd.read_parquet(path, columns=["question_id", "grade", "repeat_no"])
        except Exception:
            # ``repeat_no`` isn't needed for the estimand and may be absent in
            # future compatible exports. Parquet column projection still avoids
            # loading response text and grader explanations.
            frame = pd.read_parquet(path, columns=["question_id", "grade"])
            frame["repeat_no"] = frame.groupby("question_id").cumcount()
        frames.append(frame)
    out = pd.concat(frames, ignore_index=True)
    if out[["question_id", "grade"]].isna().any().any():
        raise ValueError("question_id and grade must be non-missing")
    out["grade"] = out["grade"].astype(float) / 10.0
    if ((out["grade"] < 0) | (out["grade"] > 1)).any():
        raise ValueError("normalized grades escaped [0, 1]")
    return out


def paired_matrices(baseline: pd.DataFrame, perturbed: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Align question IDs and return rectangular repeated-trial matrices."""
    def grouped(frame: pd.DataFrame) -> dict[str, np.ndarray]:
        result: dict[str, np.ndarray] = {}
        ordered = frame.sort_values(["question_id", "repeat_no"], kind="stable")
        for question_id, group in ordered.groupby("question_id", sort=False):
            result[str(question_id)] = group["grade"].to_numpy(dtype=float)
        return result

    base, pert = grouped(baseline), grouped(perturbed)
    common = sorted(set(base) & set(pert))
    if not common:
        raise ValueError("baseline and perturbed datasets share no question IDs")
    base_counts = {len(base[key]) for key in common}
    pert_counts = {len(pert[key]) for key in common}
    if len(base_counts) != 1 or len(pert_counts) != 1:
        raise ValueError(
            "released main-cell analysis expects a uniform trial count per condition; "
            f"found baseline={sorted(base_counts)}, perturbed={sorted(pert_counts)}"
        )
    return np.vstack([base[key] for key in common]), np.vstack([pert[key] for key in common]), common


def analyse_cell(
    baseline: np.ndarray,
    perturbed: np.ndarray,
    *,
    q: float,
    n_boot: int,
    split_reps: int,
    seed: int,
) -> dict[str, float | int]:
    adjusted = adjusted_metrics(
        baseline, perturbed, q=q, n_boot=n_boot, seed=seed,
    )
    split = split_sample_wtd(
        baseline, perturbed, q=q, n_reps=split_reps, seed=seed + 1,
    )
    absolute = crossfit_absolute_loss_tail(
        perturbed, q=q, n_reps=split_reps, seed=seed + 2,
    )
    reliability = split_half_reliability(
        baseline, perturbed, n_reps=split_reps, seed=seed + 3,
    )
    directional = directional_components(baseline, perturbed)
    item_boot = item_bootstrap(
        baseline, perturbed, q=q, n_boot=n_boot, seed=seed + 4,
    )
    return {**adjusted, **split, **absolute, **reliability, **directional, **item_boot}


def subsample_trials(values: np.ndarray, n_trials: int, rng: np.random.Generator) -> np.ndarray:
    if n_trials > values.shape[1]:
        raise ValueError("requested more trials than the released data contain")
    if n_trials == values.shape[1]:
        return values.copy()
    # Independent without-replacement subsampling within each item.
    indices = np.argsort(rng.random(values.shape), axis=1)[:, :n_trials]
    return np.take_along_axis(values, indices, axis=1)


def sensitivity_for_cell(
    baseline: np.ndarray,
    perturbed: np.ndarray,
    *,
    cell: str,
    trial_counts: list[int],
    tail_qs: list[float],
    subsample_reps: int,
    n_boot: int,
    split_reps: int,
    seed: int,
) -> list[dict]:
    rows = []
    for n_trials in trial_counts:
        if n_trials > min(baseline.shape[1], perturbed.shape[1]):
            continue
        actual_reps = 1 if n_trials == baseline.shape[1] == perturbed.shape[1] else subsample_reps
        for q in tail_qs:
            for rep in range(actual_reps):
                rep_seed = stable_seed(f"{cell}:{n_trials}:{q}:{rep}", seed)
                rng = np.random.default_rng(rep_seed)
                base_sub = subsample_trials(baseline, n_trials, rng)
                pert_sub = subsample_trials(perturbed, n_trials, rng)
                adjusted = adjusted_metrics(
                    base_sub, pert_sub, q=q, n_boot=n_boot, seed=rep_seed + 1,
                )
                split = split_sample_wtd(
                    base_sub, pert_sub, q=q, n_reps=split_reps, seed=rep_seed + 2,
                )
                absolute = crossfit_absolute_loss_tail(
                    pert_sub, q=q, n_reps=split_reps, seed=rep_seed + 3,
                )
                rows.append({
                    "cell": cell,
                    "n_trials": n_trials,
                    "tail_q": q,
                    "subsample_rep": rep,
                    "ins_raw": adjusted["ins_raw"],
                    "ins_floor": adjusted["ins_floor"],
                    "ins_adjusted": adjusted["ins_adjusted"],
                    "wtd_raw": adjusted["wtd_raw"],
                    "wtd_floor": adjusted["wtd_floor"],
                    "wtd_adjusted": adjusted["wtd_adjusted"],
                    "wtd_split": split["split_wtd"],
                    "absolute_loss_tail_raw": absolute["absolute_loss_tail_raw"],
                    "absolute_loss_tail_crossfit": absolute["absolute_loss_tail_crossfit"],
                })
    return rows


def merge_published(results: pd.DataFrame) -> pd.DataFrame:
    published = pd.read_csv(PUBLISHED)
    merged = results.merge(published, on=["benchmark", "model"], how="left", suffixes=("", "_published"))
    for metric in ("baseline_accuracy", "signed_delta", "ins_adjusted", "wtd_adjusted"):
        merged[f"{metric}_difference_from_published"] = merged[metric] - merged[f"{metric}_published"]
    return merged


def write_latex_table(results: pd.DataFrame, path: Path) -> None:
    def signed(value: float) -> str:
        return f"{0.0 if abs(value) < 0.0005 else value:+.3f}"

    lines = [
        "% Generated by python -m analysis.reanalyse_zhang; do not edit by hand.",
        "\\begin{tabular}{llrrrr}",
        "\\toprule",
        "Benchmark & Model & Baseline & $\\Delta$ & null-referenced INS & null-referenced WTD \\\\",
        "\\midrule",
    ]
    for row in results.sort_values(["benchmark", "model_label"]).itertuples(index=False):
        lines.append(
            f"{row.benchmark_label} & {row.model_label} & {row.baseline_accuracy:.3f} & "
            f"{signed(row.signed_delta)} & {row.ins_adjusted:.3f} & {row.wtd_adjusted:.3f} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}", ""])
    path.write_text("\n".join(lines))


def _style() -> None:
    plt.rcParams.update({
        "font.size": 8.5,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.dpi": 160,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })


def plot_published_comparison(results: pd.DataFrame, path: Path) -> None:
    _style()
    specs = [
        ("baseline_accuracy", "Baseline accuracy"),
        ("signed_delta", "Signed change"),
        ("ins_adjusted", "Null-referenced INS"),
        ("wtd_adjusted", "Null-referenced WTD"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 6.2))
    for ax, (metric, title) in zip(axes.ravel(), specs):
        expected = results[f"{metric}_published"]
        observed = results[metric]
        lo = float(min(expected.min(), observed.min()))
        hi = float(max(expected.max(), observed.max()))
        pad = max(0.01, 0.05 * (hi - lo or 1.0))
        ax.scatter(expected, observed, s=20, alpha=0.75, color="#4C72B0")
        ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad], color="#333333", linewidth=0.8)
        ax.set(xlabel="Published (rounded)", ylabel="Reanalysis", title=title,
               xlim=(lo - pad, hi + pad), ylim=(lo - pad, hi + pad))
        mae = float(np.mean(np.abs(observed - expected)))
        ax.text(0.04, 0.93, f"MAE={mae:.4f}", transform=ax.transAxes, va="top")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_wtd_estimators(results: pd.DataFrame, path: Path) -> None:
    _style()
    ordered = results.sort_values("wtd_adjusted").reset_index(drop=True)
    x = np.arange(len(ordered))
    fig, ax = plt.subplots(figsize=(9.0, 3.8))
    ax.scatter(x, ordered["wtd_raw"], label="raw same-sample WTD", color="#C44E52", s=20)
    ax.scatter(x, ordered["wtd_adjusted"], label="null-referenced", color="#4C72B0", s=20)
    ax.scatter(x, ordered["split_wtd"], label="held-out split-tail", color="#55A868", s=20)
    ax.axhline(0, color="#777777", linewidth=0.7)
    ax.set_xticks(x, ordered["cell"], rotation=90)
    ax.set_ylabel("Degradation probability")
    ax.set_title("Released cells: distinct WTD estimators")
    ax.legend(frameon=False, ncol=3, loc="upper left")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_sensitivity(sensitivity: pd.DataFrame, full_results: pd.DataFrame, path: Path) -> None:
    _style()
    if sensitivity.empty:
        return
    qset = sensitivity[np.isclose(sensitivity["tail_q"], 0.10)].copy()
    agg = qset.groupby("n_trials", as_index=False).agg(
        ins_adjusted=("ins_adjusted", "median"),
        wtd_adjusted=("wtd_adjusted", "median"),
        wtd_split=("wtd_split", "median"),
        absolute_tail=("absolute_loss_tail_crossfit", "median"),
    )
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.2))
    axes[0].plot(agg["n_trials"], agg["ins_adjusted"], marker="o", label="null-referenced INS", color="#4C72B0")
    axes[0].axhline(full_results["ins_adjusted"].median(), color="#4C72B0", linestyle="--", linewidth=0.8)
    axes[0].set_title("Median INS across released cells")
    axes[1].plot(agg["n_trials"], agg["wtd_adjusted"], marker="o", label="null-referenced WTD", color="#4C72B0")
    axes[1].plot(agg["n_trials"], agg["wtd_split"], marker="o", label="split WTD", color="#55A868")
    axes[1].plot(agg["n_trials"], agg["absolute_tail"], marker="o", label="case-risk tail", color="#8172B2")
    axes[1].set_title("Median tail estimates across released cells")
    for ax in axes:
        ax.set_xscale("log")
        ax.set_xticks(sorted(agg["n_trials"].unique()))
        ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        ax.set_xlabel("Trials per condition")
        ax.set_ylabel("Probability scale")
        ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("smoke", "standard"), default="standard")
    parser.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--cell", action="append", dest="cells", help="Restrict to a cell such as mmlu_pro.gpt54")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--skip-sensitivity", action="store_true")
    parser.add_argument("--seed", type=int, default=20260717)
    args = parser.parse_args()
    profiles = {
        "smoke": {
            "default_cells": ["mmlu_pro.gpt54"], "n_boot": 100, "split_reps": 50,
            "trial_counts": [2, 10, 20], "tail_qs": [0.10, 0.20],
            "subsample_reps": 2, "sensitivity_boot": 16, "sensitivity_split": 16,
        },
        "standard": {
            "default_cells": None, "n_boot": 1000, "split_reps": 200,
            "trial_counts": [2, 5, 10, 20], "tail_qs": [0.05, 0.10, 0.20],
            "subsample_reps": 10, "sensitivity_boot": 64, "sensitivity_split": 64,
        },
    }
    config = profiles[args.profile]
    lock = json.loads(args.lock.read_text())
    selected = set(args.cells or config["default_cells"] or [cell["cell"] for cell in lock["cells"]])
    cells = [cell for cell in lock["cells"] if cell["cell"] in selected]
    missing = selected - {cell["cell"] for cell in cells}
    if missing:
        raise ValueError(f"Unknown cells: {sorted(missing)}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results, sensitivity_rows, audit_rows = [], [], []
    for index, cell in enumerate(cells, 1):
        print(f"[{index}/{len(cells)}] {cell['cell']}", flush=True)
        baseline_paths, baseline_audit = fetch_dataset(
            cell["baseline_repo"], lock, cache_dir=args.cache_dir, offline=args.offline,
        )
        perturbed_paths, perturbed_audit = fetch_dataset(
            cell["perturbed_repo"], lock, cache_dir=args.cache_dir, offline=args.offline,
        )
        audit_rows.extend(baseline_audit + perturbed_audit)
        baseline, perturbed, question_ids = paired_matrices(
            read_trials(baseline_paths), read_trials(perturbed_paths)
        )
        seed = stable_seed(cell["cell"], args.seed)
        metrics = analyse_cell(
            baseline, perturbed, q=0.10, n_boot=config["n_boot"],
            split_reps=config["split_reps"], seed=seed,
        )
        results.append({
            **{key: cell[key] for key in ("cell", "benchmark", "benchmark_label", "model", "model_label",
                                          "baseline_repo", "perturbed_repo")},
            "common_question_ids": len(question_ids),
            **metrics,
        })
        if not args.skip_sensitivity:
            cell_sensitivity = sensitivity_for_cell(
                baseline, perturbed, cell=cell["cell"],
                trial_counts=config["trial_counts"], tail_qs=config["tail_qs"],
                subsample_reps=config["subsample_reps"], n_boot=config["sensitivity_boot"],
                split_reps=config["sensitivity_split"], seed=seed + 10,
            )
            for row in cell_sensitivity:
                row.update({"benchmark": cell["benchmark"], "model": cell["model"]})
            sensitivity_rows.extend(cell_sensitivity)
    result_frame = merge_published(pd.DataFrame(results))
    sensitivity_frame = pd.DataFrame(sensitivity_rows)
    audit_frame = pd.DataFrame(audit_rows).drop_duplicates(["repo", "revision", "parquet_path"])
    result_frame.to_csv(args.output_dir / "main_reanalysis.csv", index=False)
    if not sensitivity_frame.empty:
        sensitivity_frame.to_csv(args.output_dir / "trial_tail_sensitivity.csv", index=False)
    else:
        (args.output_dir / "trial_tail_sensitivity.csv").unlink(missing_ok=True)
        (args.output_dir / "trial_sensitivity.pdf").unlink(missing_ok=True)
    audit_frame.to_csv(args.output_dir / "download_audit.csv", index=False)
    write_latex_table(result_frame, args.output_dir / "main_reanalysis.tex")
    plot_published_comparison(result_frame, args.output_dir / "published_comparison.pdf")
    plot_wtd_estimators(result_frame, args.output_dir / "wtd_estimators.pdf")
    if not sensitivity_frame.empty:
        plot_sensitivity(sensitivity_frame, result_frame, args.output_dir / "trial_sensitivity.pdf")
    metadata = {
        "profile": args.profile,
        "seed": args.seed,
        "lock_file": str(args.lock),
        "code_source": lock["code"],
        "paper_source": lock["paper"],
        "cells_requested": [cell["cell"] for cell in cells],
        "config": config,
        "all_downloads_checksum_verified": bool(audit_frame["verified"].all()),
        "limitations": [
            "Subtracting the baseline pseudo-null expectation is a null-referenced diagnostic, not a general nonnull bias correction.",
            "Split WTD is unbiased for a noisy-selected set and may miss the oracle latent tail.",
            "Case-risk tail and WTD answer different questions and aren't combined.",
            "The released QA benchmarks don't instantiate the manuscript's ten CHC-style domains.",
            "Public dataset metadata exposed no license at pinning time; the cache is excluded from version control.",
            "No model generations, graders, deployment outcomes, or external validity targets are added."
        ],
    }
    (args.output_dir / "run_metadata.json").write_text(json.dumps(json_safe(metadata), indent=2) + "\n")
    print(f"Wrote released-output reanalysis to {args.output_dir}")


if __name__ == "__main__":
    main()
