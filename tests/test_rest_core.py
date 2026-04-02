from __future__ import annotations

import unittest

import numpy as np

from rest.core import (
    RestConfig,
    SlidingCovarianceWindow,
    compute_topk_eigendecomposition,
    default_phi,
    exponential_weights,
    reciprocal_weights,
    rest_step,
)
from baselines.covariance import (
    exponential_only_coordinates,
    raw_retained_coordinates,
    reciprocal_only_coordinates,
)


class TestSlidingCovarianceWindow(unittest.TestCase):
    def test_covariance_is_symmetric_psd(self) -> None:
        window = SlidingCovarianceWindow(dimension=3, window_size=4)
        points = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([0.0, 0.0, 1.0]),
            np.array([1.0, 1.0, 1.0]),
        ]
        for p in points:
            window.update(p)

        cov = window.covariance()
        self.assertTrue(np.allclose(cov, cov.T))
        evals = np.linalg.eigvalsh(cov)
        self.assertTrue(np.all(evals >= -1e-10))

    def test_topk_eigendecomposition_is_sorted(self) -> None:
        operator = np.diag([1.0, 3.0, 2.0])
        basis, evals = compute_topk_eigendecomposition(operator, rank=2)
        self.assertTrue(np.allclose(evals, np.array([3.0, 2.0])))
        self.assertEqual(basis.shape, (3, 2))


class TestRestWeights(unittest.TestCase):
    def test_reciprocal_weights_respect_clipping(self) -> None:
        evals = np.array([0.0, 1.0, 100.0])
        weights = reciprocal_weights(evals, ridge_scale=0.1, lower=0.2, upper=1.5)
        self.assertTrue(np.all(weights >= 0.2))
        self.assertTrue(np.all(weights <= 1.5))

    def test_exponential_weights_respect_clipping(self) -> None:
        evals = np.array([0.0, 1.0, 100.0])
        weights = exponential_weights(evals, ridge_scale=0.1, beta=5.0, lower=0.5, upper=2.0, phi=default_phi)
        self.assertTrue(np.all(weights >= 0.5))
        self.assertTrue(np.all(weights <= 2.0))


class TestRestStep(unittest.TestCase):
    def test_rest_step_shapes_and_condition_proxy(self) -> None:
        x = np.array([1.0, 2.0, 3.0])
        mean = np.array([0.5, 1.5, 2.5])
        operator = np.diag([3.0, 2.0, 1.0])
        basis, evals = compute_topk_eigendecomposition(operator, rank=2)
        config = RestConfig(rank=2, ridge_scale=0.5, beta=0.7)

        result = rest_step(x, mean, basis, evals, config, covariance_t=operator)
        self.assertEqual(result.coordinates.shape, (2,))
        self.assertEqual(result.rest_coordinates.shape, (2,))
        self.assertEqual(result.reciprocal_weights.shape, (2,))
        self.assertEqual(result.exponential_weights.shape, (2,))
        self.assertGreaterEqual(result.condition_proxy, 1.0)

    def test_rest_differs_from_component_baselines(self) -> None:
        x = np.array([2.0, -1.0, 0.5])
        mean = np.array([0.0, 0.0, 0.0])
        operator = np.array(
            [
                [4.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 0.25],
            ]
        )
        basis, evals = compute_topk_eigendecomposition(operator, rank=2)
        config = RestConfig(rank=2, ridge_scale=0.4, beta=0.9)
        result = rest_step(x, mean, basis, evals, config, covariance_t=operator)

        raw = raw_retained_coordinates(x, mean, basis)
        reciprocal_only = reciprocal_only_coordinates(x, mean, basis, evals, ridge_scale=0.4)
        exponential_only = exponential_only_coordinates(x, mean, basis, evals, ridge_scale=0.4, beta=0.9)

        self.assertFalse(np.allclose(result.rest_coordinates, raw))
        self.assertFalse(np.allclose(result.rest_coordinates, reciprocal_only))
        self.assertFalse(np.allclose(result.rest_coordinates, exponential_only))


if __name__ == "__main__":
    unittest.main()
