from __future__ import annotations

import numpy as np

from rest.core import default_phi, exponential_weights, reciprocal_weights


Array = np.ndarray


def raw_retained_coordinates(x_t: Array, mean_t: Array, basis_t: Array) -> Array:
    x_t = np.asarray(x_t, dtype=float)
    mean_t = np.asarray(mean_t, dtype=float)
    basis_t = np.asarray(basis_t, dtype=float)
    return basis_t.T @ (x_t - mean_t)


def pca_energy_scaled_coordinates(x_t: Array, mean_t: Array, basis_t: Array, eigenvalues_t: Array) -> Array:
    coords = raw_retained_coordinates(x_t, mean_t, basis_t)
    energy = np.sqrt(np.maximum(np.asarray(eigenvalues_t, dtype=float), 0.0))
    return energy * coords


def reciprocal_only_coordinates(
    x_t: Array,
    mean_t: Array,
    basis_t: Array,
    eigenvalues_t: Array,
    ridge_scale: float,
    reciprocal_clip: tuple[float, float] = (1e-3, 1e3),
) -> Array:
    coords = raw_retained_coordinates(x_t, mean_t, basis_t)
    weights = reciprocal_weights(eigenvalues_t, ridge_scale, reciprocal_clip[0], reciprocal_clip[1])
    return weights * coords


def exponential_only_coordinates(
    x_t: Array,
    mean_t: Array,
    basis_t: Array,
    eigenvalues_t: Array,
    ridge_scale: float,
    beta: float,
    exponential_clip: tuple[float, float] = (1e-3, 1e3),
) -> Array:
    coords = raw_retained_coordinates(x_t, mean_t, basis_t)
    weights = exponential_weights(
        eigenvalues_t,
        ridge_scale,
        beta,
        exponential_clip[0],
        exponential_clip[1],
        phi=default_phi,
    )
    return weights * coords
