"""Core estimators used by the empirical companion.

The INS/WTD pseudo-null and split-tail procedures follow the released code for
Zhang, Koyejo, and Yang (2026), pinned in ``source_manifest.json``.  They are
implemented here against NumPy arrays so the analysis doesn't import the
authors' model-serving dependencies.

Conventions
-----------
Rows are items and columns are repeated trials. ``delta`` is perturbed minus
baseline performance, matching the manuscript. ``degradation`` is its
negative, baseline minus perturbed, matching the authors' released analysis
code. Thus WTD is the mean of the largest degradation values, equivalently the
negative mean of the smallest delta values.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def _as_2d(values: np.ndarray | list[list[float]], name: str) -> np.ndarray:
    out = np.asarray(values, dtype=float)
    if out.ndim != 2 or out.shape[0] == 0 or out.shape[1] == 0:
        raise ValueError(f"{name} must be a non-empty items-by-trials array")
    if not np.all(np.isfinite(out)):
        raise ValueError(f"{name} contains non-finite values")
    if np.any((out < 0.0) | (out > 1.0)):
        raise ValueError(f"{name} values must lie in [0, 1]")
    return out


def tail_size(n_items: int, q: float) -> int:
    """Return Zhang et al.'s ceiling tail size ``ceil(q * n_items)``."""
    if n_items < 1:
        raise ValueError("n_items must be positive")
    if not 0.0 < q <= 1.0:
        raise ValueError("q must lie in (0, 1]")
    return max(1, int(math.ceil(q * n_items)))


def upper_tail_mean(values: np.ndarray, q: float) -> float:
    """Mean the largest ``ceil(q*n)`` finite values without a full sort."""
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return float("nan")
    k = tail_size(arr.size, q)
    return float(np.partition(arr, arr.size - k)[-k:].mean())


def basic_metrics(
    baseline: np.ndarray | list[list[float]],
    perturbed: np.ndarray | list[list[float]],
    *,
    q: float = 0.10,
) -> dict[str, float | int]:
    """Compute profile-independent point estimates from repeated trials."""
    base = _as_2d(baseline, "baseline")
    pert = _as_2d(perturbed, "perturbed")
    if base.shape[0] != pert.shape[0]:
        raise ValueError("baseline and perturbed must contain the same items")
    base_mean = base.mean(axis=1)
    pert_mean = pert.mean(axis=1)
    delta = pert_mean - base_mean
    degradation = -delta
    return {
        "n_items": int(base.shape[0]),
        "n_baseline_trials": int(base.shape[1]),
        "n_perturbed_trials": int(pert.shape[1]),
        "tail_q": float(q),
        "tail_k": tail_size(base.shape[0], q),
        "baseline_accuracy": float(base_mean.mean()),
        "perturbed_accuracy": float(pert_mean.mean()),
        "signed_delta": float(delta.mean()),
        "signed_degradation": float(degradation.mean()),
        "ins_raw": float(np.abs(delta).mean()),
        "wtd_raw": upper_tail_mean(degradation, q),
        "absolute_loss_mean": float((1.0 - pert_mean).mean()),
        "absolute_loss_tail_raw": upper_tail_mean(1.0 - pert_mean, q),
    }


def baseline_noise_floor(
    baseline: np.ndarray | list[list[float]],
    *,
    n_perturbed_trials: int | None = None,
    q: float = 0.10,
    n_boot: int = 1000,
    seed: int = 42,
) -> dict[str, float | int]:
    """Baseline-only bootstrap pseudo-null expectation for INS and WTD.

    For every item, two pseudo-conditions are sampled with replacement from
    that item's observed baseline pool. Their sample sizes match the real
    baseline and perturbed conditions. This is the public Zhang implementation's
    null: task-irrelevant context doesn't move the response distribution.
    """
    base = _as_2d(baseline, "baseline")
    if n_boot < 1:
        raise ValueError("n_boot must be positive")
    n_items, n_base = base.shape
    n_pert = n_base if n_perturbed_trials is None else int(n_perturbed_trials)
    if n_pert < 1:
        raise ValueError("n_perturbed_trials must be positive")
    k = tail_size(n_items, q)
    rng = np.random.default_rng(seed)
    null_degradation = np.empty((n_boot, n_items), dtype=float)
    for item in range(n_items):
        pool = base[item]
        a = pool[rng.integers(0, n_base, size=(n_boot, n_base))].mean(axis=1)
        b = pool[rng.integers(0, n_base, size=(n_boot, n_pert))].mean(axis=1)
        null_degradation[:, item] = a - b
    ins_reps = np.abs(null_degradation).mean(axis=1)
    wtd_reps = np.partition(null_degradation, n_items - k, axis=1)[:, -k:].mean(axis=1)
    return {
        "n_boot": int(n_boot),
        "ins_floor": float(ins_reps.mean()),
        "ins_floor_sd": float(ins_reps.std(ddof=1)) if n_boot > 1 else float("nan"),
        "wtd_floor": float(wtd_reps.mean()),
        "wtd_floor_sd": float(wtd_reps.std(ddof=1)) if n_boot > 1 else float("nan"),
    }


def adjusted_metrics(
    baseline: np.ndarray | list[list[float]],
    perturbed: np.ndarray | list[list[float]],
    *,
    q: float = 0.10,
    n_boot: int = 1000,
    seed: int = 42,
) -> dict[str, float | int]:
    """Return raw metrics, pseudo-null expectations, and untruncated null-referenced differences."""
    base = _as_2d(baseline, "baseline")
    pert = _as_2d(perturbed, "perturbed")
    point = basic_metrics(base, pert, q=q)
    floor = baseline_noise_floor(
        base,
        n_perturbed_trials=pert.shape[1],
        q=q,
        n_boot=n_boot,
        seed=seed,
    )
    return {
        **point,
        **floor,
        "ins_adjusted": float(point["ins_raw"] - floor["ins_floor"]),
        "wtd_adjusted": float(point["wtd_raw"] - floor["wtd_floor"]),
    }


def _random_half_means(values: np.ndarray, n_reps: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Return disjoint random-half means with shape ``(n_reps, n_items)``."""
    arr = _as_2d(values, "values")
    n_items, n_trials = arr.shape
    if n_trials < 2:
        raise ValueError("sample splitting requires at least two trials per item")
    cut = n_trials // 2
    first = np.empty((n_reps, n_items), dtype=float)
    second = np.empty((n_reps, n_items), dtype=float)
    for item in range(n_items):
        permutations = rng.permuted(np.tile(arr[item], (n_reps, 1)), axis=1)
        first[:, item] = permutations[:, :cut].mean(axis=1)
        second[:, item] = permutations[:, cut:].mean(axis=1)
    return first, second


def _select_measure_tail(select: np.ndarray, measure: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    n_reps, n_items = select.shape
    indices = np.argpartition(select, n_items - k, axis=1)[:, -k:]
    rows = np.arange(n_reps)[:, None]
    means = measure[rows, indices].mean(axis=1)
    mask = np.zeros((n_reps, n_items), dtype=bool)
    mask[rows, indices] = True
    return means, mask


def split_sample_wtd(
    baseline: np.ndarray | list[list[float]],
    perturbed: np.ndarray | list[list[float]],
    *,
    q: float = 0.10,
    n_reps: int = 200,
    seed: int = 42,
    true_degradation: np.ndarray | None = None,
) -> dict[str, float | int]:
    """Cross-fitted WTD, following Zhang et al.'s released split-tail code.

    The estimate is unbiased for the latent degradation of the noisy-selected
    set. It needn't recover the oracle tail selected using latent effects.
    ``selected_set_truth`` makes that distinction visible in simulations.
    """
    base = _as_2d(baseline, "baseline")
    pert = _as_2d(perturbed, "perturbed")
    if base.shape[0] != pert.shape[0]:
        raise ValueError("baseline and perturbed must contain the same items")
    if n_reps < 1:
        raise ValueError("n_reps must be positive")
    n_items = base.shape[0]
    k = tail_size(n_items, q)
    rng = np.random.default_rng(seed)
    b1, b2 = _random_half_means(base, n_reps, rng)
    p1, p2 = _random_half_means(pert, n_reps, rng)
    d1, d2 = b1 - p1, b2 - p2
    held_a, mask_a = _select_measure_tail(d1, d2, k)
    held_b, mask_b = _select_measure_tail(d2, d1, k)
    selected_a, _ = _select_measure_tail(d1, d1, k)
    selected_b, _ = _select_measure_tail(d2, d2, k)
    held = 0.5 * (held_a + held_b)
    selection = 0.5 * (selected_a + selected_b)
    full_deg = base.mean(axis=1) - pert.mean(axis=1)
    out: dict[str, float | int] = {
        "split_reps": int(n_reps),
        "split_wtd": float(held.mean()),
        "split_wtd_mc_sd": float(held.std(ddof=1)) if n_reps > 1 else float("nan"),
        "selection_half_wtd": float(selection.mean()),
        "naive_wtd": upper_tail_mean(full_deg, q),
    }
    out["winners_curse_naive_minus_split"] = float(out["naive_wtd"] - out["split_wtd"])
    if true_degradation is not None:
        truth = np.asarray(true_degradation, dtype=float)
        if truth.shape != (n_items,):
            raise ValueError("true_degradation must have one value per item")
        selected_truth_a = (mask_a * truth[None, :]).sum(axis=1) / k
        selected_truth_b = (mask_b * truth[None, :]).sum(axis=1) / k
        out["selected_set_truth"] = float((0.5 * (selected_truth_a + selected_truth_b)).mean())
        out["oracle_tail_truth"] = upper_tail_mean(truth, q)
    return out


def split_half_reliability(
    baseline: np.ndarray | list[list[float]],
    perturbed: np.ndarray | list[list[float]],
    *,
    n_reps: int = 200,
    seed: int = 42,
) -> dict[str, float | int]:
    """Reliability of item degradation across disjoint trial halves."""
    base = _as_2d(baseline, "baseline")
    pert = _as_2d(perturbed, "perturbed")
    if base.shape[0] != pert.shape[0]:
        raise ValueError("baseline and perturbed must contain the same items")
    rng = np.random.default_rng(seed)
    b1, b2 = _random_half_means(base, n_reps, rng)
    p1, p2 = _random_half_means(pert, n_reps, rng)
    d1, d2 = b1 - p1, b2 - p2
    rs = np.array([pearson_profile(d1[row], d2[row]) for row in range(n_reps)])
    finite = rs[np.isfinite(rs)]
    mean_r = float(finite.mean()) if finite.size else float("nan")
    spearman_brown = (
        float(2.0 * mean_r / (1.0 + mean_r))
        if math.isfinite(mean_r) and mean_r > -1.0
        else float("nan")
    )
    return {
        "split_half_reps": int(n_reps),
        "split_half_r": mean_r,
        "split_half_r_sd": float(finite.std(ddof=1)) if finite.size > 1 else float("nan"),
        "split_half_undefined_rate": float(1.0 - finite.size / n_reps),
        "spearman_brown_reliability": spearman_brown,
    }


def crossfit_absolute_loss_tail(
    perturbed: np.ndarray | list[list[float]],
    *,
    q: float = 0.10,
    n_reps: int = 200,
    seed: int = 42,
    true_loss: np.ndarray | None = None,
) -> dict[str, float | int]:
    """Select and estimate the worst absolute perturbed-condition loss tail.

    This is deliberately not WTD. It measures poor absolute performance even
    when the system is stably poor and its condition-to-condition change is 0.
    """
    pert = _as_2d(perturbed, "perturbed")
    n_items = pert.shape[0]
    k = tail_size(n_items, q)
    rng = np.random.default_rng(seed)
    p1, p2 = _random_half_means(pert, n_reps, rng)
    loss1, loss2 = 1.0 - p1, 1.0 - p2
    held_a, mask_a = _select_measure_tail(loss1, loss2, k)
    held_b, mask_b = _select_measure_tail(loss2, loss1, k)
    held = 0.5 * (held_a + held_b)
    full_loss = 1.0 - pert.mean(axis=1)
    out: dict[str, float | int] = {
        "absolute_tail_q": float(q),
        "absolute_tail_k": int(k),
        "absolute_loss_tail_raw": upper_tail_mean(full_loss, q),
        "absolute_loss_tail_crossfit": float(held.mean()),
        "absolute_loss_tail_mc_sd": float(held.std(ddof=1)) if n_reps > 1 else float("nan"),
    }
    if true_loss is not None:
        truth = np.asarray(true_loss, dtype=float)
        if truth.shape != (n_items,):
            raise ValueError("true_loss must have one value per item")
        selected_a = (mask_a * truth[None, :]).sum(axis=1) / k
        selected_b = (mask_b * truth[None, :]).sum(axis=1) / k
        out["absolute_selected_set_truth"] = float((0.5 * (selected_a + selected_b)).mean())
        out["absolute_oracle_tail_truth"] = upper_tail_mean(truth, q)
    return out


def pearson_profile(x: np.ndarray, y: np.ndarray, *, atol: float = 1e-12) -> float:
    """Pearson profile correlation, undefined for either constant profile."""
    a = np.asarray(x, dtype=float)
    b = np.asarray(y, dtype=float)
    if a.shape != b.shape or a.ndim != 1 or a.size < 3:
        raise ValueError("profiles must be equal-length one-dimensional arrays of length >= 3")
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        return float("nan")
    if float(np.std(a)) <= atol or float(np.std(b)) <= atol:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def json_safe(value: Any) -> Any:
    """Recursively replace NumPy scalars and non-finite floats for strict JSON."""
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value
