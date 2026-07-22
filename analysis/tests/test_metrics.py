from __future__ import annotations

import math
import unittest

import numpy as np

from analysis.metrics import (
    adjusted_metrics,
    basic_metrics,
    crossfit_absolute_loss_tail,
    directional_components,
    item_bootstrap,
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

    def test_directional_components_satisfy_the_identities(self) -> None:
        rng = np.random.default_rng(3)
        baseline = rng.uniform(0.2, 0.8, size=(60, 4))
        perturbed = np.clip(baseline + rng.normal(0.0, 0.1, size=(60, 4)), 0.0, 1.0)
        point = basic_metrics(baseline, perturbed, q=0.10)
        parts = directional_components(baseline, perturbed)
        self.assertAlmostEqual(parts["f_plus"] - parts["f_minus"], point["signed_delta"])
        self.assertAlmostEqual(parts["f_plus"] + parts["f_minus"], point["ins_raw"])
        self.assertGreaterEqual(parts["f_plus"], 0.0)
        self.assertGreaterEqual(parts["f_minus"], 0.0)

    def test_directional_components_are_transition_proportions(self) -> None:
        baseline = np.zeros((10, 1))
        perturbed = np.zeros((10, 1))
        perturbed[:3] = 1.0
        parts = directional_components(baseline, perturbed)
        self.assertAlmostEqual(parts["f_plus"], 0.3)
        self.assertAlmostEqual(parts["f_minus"], 0.0)

    def test_item_bootstrap_brackets_the_point_estimate(self) -> None:
        rng = np.random.default_rng(11)
        baseline = rng.uniform(0.3, 0.7, size=(120, 6))
        perturbed = np.clip(baseline - rng.uniform(0.0, 0.2, size=(120, 6)), 0.0, 1.0)
        point = basic_metrics(baseline, perturbed, q=0.10)
        boot = item_bootstrap(baseline, perturbed, q=0.10, n_boot=400, seed=5)
        for name in ("signed_delta", "ins_raw", "wtd_raw"):
            self.assertLessEqual(boot[f"{name}_boot_lo"], point[name])
            self.assertGreaterEqual(boot[f"{name}_boot_hi"], point[name])
            self.assertGreater(boot[f"{name}_boot_sd"], 0.0)

    def test_item_bootstrap_collapses_for_identical_items(self) -> None:
        baseline = np.full((40, 3), 0.5)
        perturbed = np.full((40, 3), 0.3)
        boot = item_bootstrap(baseline, perturbed, q=0.10, n_boot=200, seed=7)
        self.assertAlmostEqual(boot["signed_delta_boot_sd"], 0.0)
        self.assertAlmostEqual(boot["wtd_raw_boot_lo"], 0.2)
        self.assertAlmostEqual(boot["wtd_raw_boot_hi"], 0.2)

    def test_response_noise_inflates_the_raw_tail_above_the_latent_tail(self) -> None:
        from analysis.simulate_bootstrap_coverage import population_truths

        truths = population_truths(population=40_000, n_trials=20, q=0.10, seed=3)
        self.assertGreater(
            truths["population_raw_wtd"], truths["population_latent_wtd"] + 0.05
        )

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
