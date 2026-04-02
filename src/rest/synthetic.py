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


def sparse_high_noise_stream(
    *,
    steps: int,
    dimension: int = 10,
    signal_dims: int = 2,
    signal_scale: float = 0.5,
    noise_scale: float = 1.2,
    sparsity_prob: float = 0.15,
    seed: int = 29,
) -> Iterator[Array]:
    if dimension < signal_dims:
        raise ValueError("dimension must be at least signal_dims")
    rng = np.random.default_rng(seed)

    for t in range(steps):
        point = rng.normal(scale=noise_scale, size=dimension)
        mask = rng.random(signal_dims) < sparsity_prob
        signal = np.zeros(signal_dims, dtype=float)
        if np.any(mask):
            signal[mask] = signal_scale * rng.normal(size=int(np.sum(mask)))
        point[:signal_dims] += signal
        if t % 17 == 0:
            point[:signal_dims] += 0.25 * np.array([1.0, -1.0])[:signal_dims]
        yield point


def regime_switch_stream(
    *,
    steps: int,
    dimension: int = 6,
    change_fraction: float = 0.5,
    pre_major_scale: float = 2.5,
    post_major_scale: float = 0.9,
    pre_minor_scale: float = 0.4,
    post_minor_scale: float = 2.2,
    noise_scale: float = 0.03,
    seed: int = 37,
) -> Iterator[Array]:
    if dimension < 2:
        raise ValueError("dimension must be at least 2")
    rng = np.random.default_rng(seed)
    change_index = max(1, min(steps - 1, int(change_fraction * steps)))

    for t in range(steps):
        if t < change_index:
            scales = np.array([pre_major_scale, pre_minor_scale], dtype=float)
            theta = 0.02 * t
        else:
            scales = np.array([post_major_scale, post_minor_scale], dtype=float)
            theta = 0.8 + 0.06 * (t - change_index)
        rot = _rotation_matrix(theta)
        sample2 = rot @ (scales * rng.normal(size=2))
        point = np.zeros(dimension, dtype=float)
        point[:2] = sample2
        point += rng.normal(scale=noise_scale, size=dimension)
        yield point
