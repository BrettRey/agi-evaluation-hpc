from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

from analysis.pin_sources import expand_cells
from analysis.reanalyse_zhang import paired_matrices
from analysis.simulate_instability import latent_scenario, truth_metrics
from analysis.simulate_pss import domain_profiles


HERE = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_source_manifest_expands_to_32_unique_cells_and_64_repos(self) -> None:
        manifest = json.loads((HERE / "source_manifest.json").read_text())
        cells = expand_cells(manifest)
        self.assertEqual(len(cells), 32)
        self.assertEqual(len({cell["cell"] for cell in cells}), 32)
        repos = {cell[key] for cell in cells for key in ("baseline_repo", "perturbed_repo")}
        self.assertEqual(len(repos), 64)

    def test_locked_files_have_revisions_and_lfs_hashes(self) -> None:
        lock = json.loads((HERE / "source_manifest.lock.json").read_text())
        self.assertEqual(len(lock["datasets"]), 64)
        for source in lock["datasets"].values():
            self.assertEqual(len(source["revision"]), 40)
            self.assertFalse(source["private"])
            self.assertFalse(source["gated"])
            for file_info in source["parquet"]:
                self.assertEqual(len(file_info["lfs_sha256"]), 64)

    def test_published_table_has_all_cells(self) -> None:
        frame = pd.read_csv(HERE / "published_main_results.csv")
        self.assertEqual(len(frame), 32)
        self.assertFalse(frame.duplicated(["benchmark", "model"]).any())

    def test_pairing_aligns_question_ids_and_normalized_trials(self) -> None:
        baseline = pd.DataFrame({
            "question_id": [2, 1, 2, 1], "grade": [0.2, 0.1, 0.4, 0.3],
            "repeat_no": [0, 0, 1, 1],
        })
        perturbed = pd.DataFrame({
            "question_id": [1, 2, 1, 2], "grade": [0.5, 0.6, 0.7, 0.8],
            "repeat_no": [0, 0, 1, 1],
        })
        b, p, ids = paired_matrices(baseline, perturbed)
        self.assertEqual(ids, ["1", "2"])
        np.testing.assert_allclose(b, [[0.1, 0.3], [0.2, 0.4]])
        np.testing.assert_allclose(p, [[0.5, 0.7], [0.6, 0.8]])

    def test_sparse_collapse_truth(self) -> None:
        p0, p1, _ = latent_scenario("sparse_collapse", 100, 12)
        truth = truth_metrics(p0, p1, 0.10)
        self.assertAlmostEqual(truth["signed_delta"], -0.055)
        self.assertAlmostEqual(truth["ins"], 0.055)
        self.assertAlmostEqual(truth["wtd"], 0.55)

    def test_profile_correlation_scenarios_have_expected_latent_correlations(self) -> None:
        from analysis.metrics import pearson_profile

        base, pert, _ = domain_profiles("moderate_transport", 1)
        self.assertAlmostEqual(pearson_profile(base, pert), 0.65, places=12)
        base, pert, _ = domain_profiles("flat_perturbed", 1)
        self.assertTrue(np.isnan(pearson_profile(base, pert)))


if __name__ == "__main__":
    unittest.main()
