from __future__ import annotations

import math
import unittest

import numpy as np

from analysis.metrics import (
    adjusted_metrics,
    basic_metrics,
    crossfit_absolute_loss_tail,
    pearson_profile,
    split_half_reliability,
    split_sample_wtd,
    tail_size,
    upper_tail_mean,
)


class MetricTests(unittest.TestCase):
    def test_tail_uses_ceiling_cardinality(self) -> None:
        self.assertEqual(tail_size(11, 0.10), 2)
        self.assertAlmostEqual(upper_tail_mean(np.arange(11), 0.10), 9.5)

    def test_exact_cancellation(self) -> None:
        baseline = np.full((100, 1), 0.60)
        perturbed = baseline.copy()
        perturbed[:50] -= 0.20
        perturbed[50:] += 0.20
        result = basic_metrics(baseline, perturbed, q=0.10)
        self.assertAlmostEqual(result["signed_delta"], 0.0)
        self.assertAlmostEqual(result["ins_raw"], 0.20)
        self.assertAlmostEqual(result["wtd_raw"], 0.20)

    def test_constant_baseline_has_zero_null_floor(self) -> None:
        baseline = np.ones((20, 6))
        perturbed = np.ones((20, 6))
        result = adjusted_metrics(baseline, perturbed, n_boot=20, seed=1)
        self.assertEqual(result["ins_floor"], 0.0)
        self.assertEqual(result["wtd_floor"], 0.0)
        self.assertEqual(result["ins_adjusted"], 0.0)
        self.assertEqual(result["wtd_adjusted"], 0.0)

    def test_untruncated_adjustment_can_be_negative(self) -> None:
        baseline = np.tile([0.0, 1.0], (40, 4))
        perturbed = baseline.copy()
        result = adjusted_metrics(baseline, perturbed, n_boot=100, seed=4)
        self.assertLess(result["ins_adjusted"], 0.0)
        self.assertLess(result["wtd_adjusted"], 0.0)

    def test_split_tail_exact_for_deterministic_items(self) -> None:
        baseline = np.ones((20, 8))
        perturbed = np.ones((20, 8))
        perturbed[:2] = 0.0
        truth = np.zeros(20)
        truth[:2] = 1.0
        result = split_sample_wtd(
            baseline, perturbed, q=0.10, n_reps=10, seed=2,
            true_degradation=truth,
        )
        self.assertAlmostEqual(result["split_wtd"], 1.0)
        self.assertAlmostEqual(result["selected_set_truth"], 1.0)
        self.assertAlmostEqual(result["oracle_tail_truth"], 1.0)

    def test_absolute_tail_detects_stable_failure(self) -> None:
        perturbed = np.zeros((20, 6))
        result = crossfit_absolute_loss_tail(perturbed, q=0.10, n_reps=10, seed=3)
        self.assertAlmostEqual(result["absolute_loss_tail_raw"], 1.0)
        self.assertAlmostEqual(result["absolute_loss_tail_crossfit"], 1.0)

    def test_profile_correlation_and_constant_guard(self) -> None:
        x = np.arange(10, dtype=float)
        self.assertAlmostEqual(pearson_profile(x, x + 5), 1.0)
        self.assertTrue(math.isnan(pearson_profile(x, np.ones(10))))

    def test_split_half_reliability_is_one_for_deterministic_effects(self) -> None:
        baseline = np.ones((20, 6))
        perturbed = np.vstack([np.zeros((10, 6)), np.ones((10, 6))])
        result = split_half_reliability(baseline, perturbed, n_reps=5, seed=9)
        self.assertAlmostEqual(result["split_half_r"], 1.0)
        self.assertAlmostEqual(result["spearman_brown_reliability"], 1.0)


if __name__ == "__main__":
    unittest.main()
