from __future__ import annotations

from typing import Iterator

import numpy as np


Array = np.ndarray


def _rotation_matrix(theta: float) -> Array:
    c = float(np.cos(theta))
    s = float(np.sin(theta))
    return np.array([[c, -s], [s, c]], dtype=float)


def drifting_low_rank_stream(
    *,
    steps: int,
    dimension: int = 6,
    noise_scale: float = 0.05,
    drift_speed: float = 0.03,
    seed: int = 7,
) -> Iterator[Array]:
    if dimension < 2:
        raise ValueError("dimension must be at least 2")
    rng = np.random.default_rng(seed)
    base = np.zeros((dimension, 2), dtype=float)
    base[0, 0] = 1.0
    base[1, 1] = 1.0

    for t in range(steps):
        rotation = _rotation_matrix(drift_speed * t)
        basis = base.copy()
        basis[:2, :2] = rotation
        coeffs = rng.normal(size=2)
        coeffs[0] *= 2.0
        point = basis @ coeffs
        point += rng.normal(scale=noise_scale, size=dimension)
        yield point


def rotating_anisotropic_gaussian_stream(
    *,
    steps: int,
    dimension: int = 6,
    major_scale: float = 3.0,
    minor_scale: float = 0.5,
    rotation_speed: float = 0.05,
    noise_floor: float = 0.02,
    seed: int = 11,
) -> Iterator[Array]:
    if dimension < 2:
        raise ValueError("dimension must be at least 2")
    rng = np.random.default_rng(seed)
    diag = np.array([major_scale, minor_scale], dtype=float)

    for t in range(steps):
        rot = _rotation_matrix(rotation_speed * t)
        sample2 = rot @ (diag * rng.normal(size=2))
        point = np.zeros(dimension, dtype=float)
        point[:2] = sample2
        point += rng.normal(scale=noise_floor, size=dimension)
        yield point


def deforming_manifold_stream(
    *,
    steps: int,
    dimension: int = 6,
    deformation_speed: float = 0.02,
    noise_scale: float = 0.03,
    seed: int = 19,
) -> Iterator[Array]:
    if dimension < 3:
        raise ValueError("dimension must be at least 3")
    rng = np.random.default_rng(seed)

    for t in range(steps):
        u = 2.0 * np.pi * (t / max(steps - 1, 1))
        amp = 1.0 + 0.5 * np.sin(deformation_speed * t)
        x = np.cos(u)
        y = np.sin(u)
        z = amp * np.sin(2.0 * u)
        point = np.zeros(dimension, dtype=float)
        point[:3] = np.array([x, y, z], dtype=float)
        if dimension > 3:
            point[3] = amp * np.cos(3.0 * u)
        point += rng.normal(scale=noise_scale, size=dimension)
        yield point
