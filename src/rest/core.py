from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Callable, Deque, Dict, Optional

import numpy as np


Array = np.ndarray


def clip_scalar(value: float, lower: float, upper: float) -> float:
    return float(min(upper, max(lower, value)))


@dataclass(frozen=True)
class RestConfig:
    rank: int
    ridge_scale: float
    beta: float
    reciprocal_clip: tuple[float, float] = (1e-3, 1e3)
    exponential_clip: tuple[float, float] = (1e-3, 1e3)


@dataclass
class RestStepResult:
    mean: Array
    covariance: Array
    basis: Array
    eigenvalues: Array
    centered: Array
    coordinates: Array
    reciprocal_weights: Array
    exponential_weights: Array
    composite_weights: Array
    rest_coordinates: Array
    condition_proxy: float


class SlidingCovarianceWindow:
    """Simple sliding-window covariance operator for streaming experiments."""

    def __init__(self, dimension: int, window_size: int) -> None:
        if dimension <= 0:
            raise ValueError("dimension must be positive")
        if window_size < 2:
            raise ValueError("window_size must be at least 2")
        self.dimension = dimension
        self.window_size = window_size
        self._window: Deque[Array] = deque(maxlen=window_size)

    def update(self, x: Array) -> None:
        x = np.asarray(x, dtype=float)
        if x.shape != (self.dimension,):
            raise ValueError(f"expected shape {(self.dimension,)}, got {x.shape}")
        self._window.append(x.copy())

    @property
    def ready(self) -> bool:
        return len(self._window) >= self.window_size

    @property
    def count(self) -> int:
        return len(self._window)

    def stacked(self) -> Array:
        if not self._window:
            raise ValueError("window is empty")
        return np.vstack(self._window)

    def mean(self) -> Array:
        return np.mean(self.stacked(), axis=0)

    def covariance(self) -> Array:
        xs = self.stacked()
        mu = np.mean(xs, axis=0)
        centered = xs - mu
        return (centered.T @ centered) / xs.shape[0]


def compute_topk_eigendecomposition(operator: Array, rank: int) -> tuple[Array, Array]:
    operator = np.asarray(operator, dtype=float)
    if operator.ndim != 2 or operator.shape[0] != operator.shape[1]:
        raise ValueError("operator must be square")
    d = operator.shape[0]
    if not 1 <= rank <= d:
        raise ValueError("rank must satisfy 1 <= rank <= dimension")

    evals, evecs = np.linalg.eigh(operator)
    order = np.argsort(evals)[::-1]
    evals = evals[order]
    evecs = evecs[:, order]

    evals = np.maximum(evals[:rank], 0.0)
    basis = evecs[:, :rank]

    # deterministic sign convention for reproducibility
    for j in range(basis.shape[1]):
        pivot = int(np.argmax(np.abs(basis[:, j])))
        if basis[pivot, j] < 0:
            basis[:, j] *= -1.0

    return basis, evals


def default_phi(eigenvalues: Array, ridge_scale: float) -> Array:
    eigenvalues = np.asarray(eigenvalues, dtype=float)
    if ridge_scale <= 0:
        raise ValueError("ridge_scale must be positive")
    return eigenvalues / (eigenvalues + ridge_scale)


def reciprocal_weights(
    eigenvalues: Array,
    ridge_scale: float,
    lower: float,
    upper: float,
) -> Array:
    eigenvalues = np.asarray(eigenvalues, dtype=float)
    if ridge_scale <= 0:
        raise ValueError("ridge_scale must be positive")
    if not (0 < lower <= upper):
        raise ValueError("invalid reciprocal clipping bounds")
    raw = np.power(eigenvalues + ridge_scale, -0.5)
    return np.clip(raw, lower, upper)


def exponential_weights(
    eigenvalues: Array,
    ridge_scale: float,
    beta: float,
    lower: float,
    upper: float,
    phi: Callable[[Array, float], Array] = default_phi,
) -> Array:
    eigenvalues = np.asarray(eigenvalues, dtype=float)
    if not (0 < lower <= upper):
        raise ValueError("invalid exponential clipping bounds")
    shaped = phi(eigenvalues, ridge_scale)
    raw = np.exp(beta * shaped)
    return np.clip(raw, lower, upper)


def rest_step(
    x_t: Array,
    mean_t: Array,
    basis_t: Array,
    eigenvalues_t: Array,
    config: RestConfig,
    phi: Callable[[Array, float], Array] = default_phi,
    covariance_t: Optional[Array] = None,
) -> RestStepResult:
    x_t = np.asarray(x_t, dtype=float)
    mean_t = np.asarray(mean_t, dtype=float)
    basis_t = np.asarray(basis_t, dtype=float)
    eigenvalues_t = np.asarray(eigenvalues_t, dtype=float)

    if x_t.shape != mean_t.shape:
        raise ValueError("x_t and mean_t must have the same shape")
    if basis_t.ndim != 2:
        raise ValueError("basis_t must be a matrix")
    if basis_t.shape[0] != x_t.shape[0]:
        raise ValueError("basis dimension must match data dimension")
    if basis_t.shape[1] != eigenvalues_t.shape[0]:
        raise ValueError("basis width must match eigenvalue count")
    if config.rank != basis_t.shape[1]:
        raise ValueError("config.rank must match retained basis width")

    centered = x_t - mean_t
    coordinates = basis_t.T @ centered

    inv_weights = reciprocal_weights(
        eigenvalues_t,
        config.ridge_scale,
        config.reciprocal_clip[0],
        config.reciprocal_clip[1],
    )
    exp_weights = exponential_weights(
        eigenvalues_t,
        config.ridge_scale,
        config.beta,
        config.exponential_clip[0],
        config.exponential_clip[1],
        phi=phi,
    )
    composite = inv_weights * exp_weights
    rest_coordinates = composite * coordinates

    min_weight = float(np.min(composite))
    max_weight = float(np.max(composite))
    condition_proxy = float(max_weight / min_weight) if min_weight > 0 else float("inf")

    if covariance_t is None:
        covariance_t = np.zeros((x_t.shape[0], x_t.shape[0]), dtype=float)

    return RestStepResult(
        mean=mean_t,
        covariance=np.asarray(covariance_t, dtype=float),
        basis=basis_t,
        eigenvalues=eigenvalues_t,
        centered=centered,
        coordinates=coordinates,
        reciprocal_weights=inv_weights,
        exponential_weights=exp_weights,
        composite_weights=composite,
        rest_coordinates=rest_coordinates,
        condition_proxy=condition_proxy,
    )
