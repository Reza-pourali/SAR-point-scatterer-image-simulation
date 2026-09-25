import sys
import unittest
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sar_scatterer_sim.model import (
    CASES,
    image_statistics,
    simulate_image,
    theoretical_coherent_component,
)


class TestSarScattererSimulation(unittest.TestCase):
    def test_reproducibility(self):
        a1, p1 = simulate_image("case2", "fixed", rows=20, cols=20, seed=7)
        a2, p2 = simulate_image("case2", "fixed", rows=20, cols=20, seed=7)
        np.testing.assert_allclose(a1, a2)
        np.testing.assert_allclose(p1, p2)

    def test_output_shapes(self):
        a, p = simulate_image("case1", "random", rows=17, cols=19, n_scatterers=10)
        self.assertEqual(a.shape, (17, 19))
        self.assertEqual(p.shape, (17, 19))

    def test_narrow_phase_has_larger_mean_amplitude_than_full_phase(self):
        full, _ = simulate_image("case1", "fixed", rows=100, cols=100, seed=3)
        narrow, _ = simulate_image("case2", "fixed", rows=100, cols=100, seed=3)
        self.assertGreater(narrow.mean(), full.mean() * 5.0)

    def test_medium_phase_is_between_full_and_narrow(self):
        full, _ = simulate_image("case1", "fixed", rows=80, cols=80, seed=11)
        narrow, _ = simulate_image("case2", "fixed", rows=80, cols=80, seed=11)
        medium, _ = simulate_image("case3", "fixed", rows=80, cols=80, seed=11)
        self.assertLess(full.mean(), medium.mean())
        self.assertLess(medium.mean(), narrow.mean())

    def test_random_amplitude_reduces_coherent_component(self):
        fixed = theoretical_coherent_component("case2", "fixed")
        random = theoretical_coherent_component("case2", "random")
        self.assertAlmostEqual(random, 0.5 * fixed, places=10)

    def test_phase_ranges_are_correct(self):
        self.assertAlmostEqual(CASES["case1"].phase_half_range, np.pi)
        self.assertAlmostEqual(CASES["case2"].phase_half_range, np.pi / 5)
        self.assertAlmostEqual(CASES["case3"].phase_half_range, 2 * np.pi / 5)

    def test_statistics_are_finite(self):
        a, p = simulate_image("case3", "random", rows=20, cols=20, seed=9)
        stats = image_statistics(a, p)
        self.assertTrue(all(np.isfinite(v) for v in stats.values()))


if __name__ == "__main__":
    unittest.main()
