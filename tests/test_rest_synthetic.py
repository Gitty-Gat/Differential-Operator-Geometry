from __future__ import annotations

import unittest

import numpy as np

from rest.synthetic import (
    deforming_manifold_stream,
    drifting_low_rank_stream,
    rotating_anisotropic_gaussian_stream,
)


class TestSyntheticStreams(unittest.TestCase):
    def test_drifting_low_rank_stream_shapes(self) -> None:
        xs = list(drifting_low_rank_stream(steps=5, dimension=6, seed=1))
        self.assertEqual(len(xs), 5)
        self.assertTrue(all(x.shape == (6,) for x in xs))

    def test_rotating_gaussian_stream_shapes(self) -> None:
        xs = list(rotating_anisotropic_gaussian_stream(steps=5, dimension=6, seed=2))
        self.assertEqual(len(xs), 5)
        self.assertTrue(all(x.shape == (6,) for x in xs))

    def test_deforming_manifold_stream_shapes(self) -> None:
        xs = list(deforming_manifold_stream(steps=5, dimension=6, seed=3))
        self.assertEqual(len(xs), 5)
        self.assertTrue(all(x.shape == (6,) for x in xs))
        self.assertFalse(np.allclose(xs[0], xs[-1]))


if __name__ == "__main__":
    unittest.main()
