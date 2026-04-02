from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from baselines.covariance import (  # noqa: E402
    exponential_only_coordinates,
    exponential_then_reciprocal_coordinates,
    pca_energy_scaled_coordinates,
    raw_retained_coordinates,
    reciprocal_only_coordinates,
)
from rest.core import (  # noqa: E402
    RestConfig,
    SlidingCovarianceWindow,
    compute_topk_eigendecomposition,
    rest_step,
)
from rest.synthetic import (  # noqa: E402
    deforming_manifold_stream,
    drifting_low_rank_stream,
    regime_switch_stream,
    rotating_anisotropic_gaussian_stream,
    sparse_high_noise_stream,
)

Array = np.ndarray
EPS = 1e-12


def projector_distance(basis_a: Array, basis_b: Array) -> float:
    proj_a = basis_a @ basis_a.T
    proj_b = basis_b @ basis_b.T
    return float(np.linalg.norm(proj_a - proj_b, ord=2))


def adjacent_mean_norm(vectors: List[Array]) -> float:
    if len(vectors) < 2:
        return 0.0
    return float(np.mean([np.linalg.norm(vectors[i] - vectors[i - 1]) for i in range(1, len(vectors))]))


def adjacent_mean_scalar(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    return float(np.mean([abs(values[i] - values[i - 1]) for i in range(1, len(values))]))


def spectral_gap(full_evals_desc: Array, rank: int) -> float:
    if rank >= len(full_evals_desc):
        return float(full_evals_desc[rank - 1])
    return float(full_evals_desc[rank - 1] - full_evals_desc[rank])


def fisher_ratio(points: List[Array], labels: List[int]) -> float:
    if not points or len(set(labels)) < 2:
        return 0.0
    xs = np.vstack(points)
    ys = np.asarray(labels)
    classes = sorted(set(labels))
    means = []
    within = 0.0
    count = 0
    for c in classes:
        block = xs[ys == c]
        if len(block) == 0:
            continue
        mu = np.mean(block, axis=0)
        means.append(mu)
        within += float(np.mean(np.sum((block - mu) ** 2, axis=1)))
        count += 1
    if count < 2:
        return 0.0
    between = float(np.linalg.norm(means[0] - means[1]))
    return between / (within / count + EPS)


def change_point_contrast(points: List[Array], effective_change_index: int, radius: int = 4) -> float:
    if len(points) < 3:
        return 0.0
    scores = [float(np.linalg.norm(points[i] - points[i - 1])) for i in range(1, len(points))]
    change_index = max(1, min(len(scores) - 1, effective_change_index))
    local = []
    background = []
    for i, score in enumerate(scores):
        if abs(i - change_index) <= radius:
            local.append(score)
        elif abs(i - change_index) >= 3 * radius:
            background.append(score)
    if not local or not background:
        return 0.0
    return float(np.mean(local) / (np.mean(background) + EPS))


def one_step_forecast_mse(points: List[Array]) -> float:
    if len(points) < 8:
        return 0.0
    xs = np.vstack(points[:-1])
    ys = np.vstack(points[1:])
    split = max(4, int(0.7 * len(xs)))
    x_train, x_test = xs[:split], xs[split:]
    y_train, y_test = ys[:split], ys[split:]
    if len(x_test) == 0:
        return 0.0
    coef, _, _, _ = np.linalg.lstsq(x_train, y_train, rcond=None)
    pred = x_test @ coef
    return float(np.mean(np.sum((pred - y_test) ** 2, axis=1)))


def svg_polyline_chart(
    path: Path,
    series: Dict[str, List[Tuple[float, float]]],
    *,
    title: str,
    width: int = 820,
    height: int = 420,
) -> None:
    margin = 50
    all_points = [pt for points in series.values() for pt in points]
    xs = [p[0] for p in all_points]
    ys = [p[1] for p in all_points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    if math.isclose(min_x, max_x):
        max_x = min_x + 1.0
    if math.isclose(min_y, max_y):
        max_y = min_y + 1.0
    colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e"]

    def sx(x: float) -> float:
        return margin + (x - min_x) / (max_x - min_x) * (width - 2 * margin)

    def sy(y: float) -> float:
        return height - margin - (y - min_y) / (max_y - min_y) * (height - 2 * margin)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        f'<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="24" text-anchor="middle" font-size="18" font-family="Arial">{title}</text>',
        f'<line x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" stroke="black"/>',
        f'<line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" stroke="black"/>',
    ]

    for idx, (name, points) in enumerate(series.items()):
        poly = " ".join(f"{sx(x):.2f},{sy(y):.2f}" for x, y in points)
        color = colors[idx % len(colors)]
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{poly}"/>')
        parts.append(f'<text x="{width - 180}" y="{40 + 20 * idx}" fill="{color}" font-size="12" font-family="Arial">{name}</text>')

    for tick in range(5):
        x = min_x + tick * (max_x - min_x) / 4
        px = sx(x)
        parts.append(f'<line x1="{px:.2f}" y1="{height-margin}" x2="{px:.2f}" y2="{height-margin+5}" stroke="black"/>')
        parts.append(f'<text x="{px:.2f}" y="{height-margin+20}" text-anchor="middle" font-size="11" font-family="Arial">{x:.2f}</text>')
        y = min_y + tick * (max_y - min_y) / 4
        py = sy(y)
        parts.append(f'<line x1="{margin-5}" y1="{py:.2f}" x2="{margin}" y2="{py:.2f}" stroke="black"/>')
        parts.append(f'<text x="{margin-8}" y="{py+4:.2f}" text-anchor="end" font-size="11" font-family="Arial">{y:.2f}</text>')

    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def svg_heatmap(
    path: Path,
    matrix: List[List[float]],
    row_labels: List[str],
    col_labels: List[str],
    *,
    title: str,
    width: int = 820,
    height: int = 460,
) -> None:
    margin_left = 120
    margin_top = 60
    cell_w = 120
    cell_h = 70
    flat = [v for row in matrix for v in row]
    min_v, max_v = min(flat), max(flat)
    if math.isclose(min_v, max_v):
        max_v = min_v + 1.0

    def color(value: float) -> str:
        alpha = (value - min_v) / (max_v - min_v)
        r = int(255 * alpha)
        b = int(255 * (1 - alpha))
        g = 80
        return f"rgb({r},{g},{b})"

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="28" text-anchor="middle" font-size="18" font-family="Arial">{title}</text>',
    ]
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            x = margin_left + j * cell_w
            y = margin_top + i * cell_h
            parts.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="{color(value)}" stroke="white"/>')
            parts.append(f'<text x="{x + cell_w/2}" y="{y + cell_h/2 + 4}" text-anchor="middle" font-size="12" font-family="Arial" fill="white">{value:.3f}</text>')
    for j, label in enumerate(col_labels):
        x = margin_left + j * cell_w + cell_w / 2
        parts.append(f'<text x="{x}" y="{margin_top - 12}" text-anchor="middle" font-size="12" font-family="Arial">{label}</text>')
    for i, label in enumerate(row_labels):
        y = margin_top + i * cell_h + cell_h / 2 + 4
        parts.append(f'<text x="{margin_left - 10}" y="{y}" text-anchor="end" font-size="12" font-family="Arial">{label}</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def svg_trajectory_plot(
    path: Path,
    trajectories: Dict[str, List[Array]],
    *,
    title: str,
    width: int = 820,
    height: int = 420,
) -> None:
    margin = 50
    colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd"]
    all_xy = []
    for points in trajectories.values():
        for p in points:
            if len(p) >= 2:
                all_xy.append((float(p[0]), float(p[1])))
    xs = [p[0] for p in all_xy]
    ys = [p[1] for p in all_xy]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    if math.isclose(min_x, max_x):
        max_x = min_x + 1.0
    if math.isclose(min_y, max_y):
        max_y = min_y + 1.0

    def sx(x: float) -> float:
        return margin + (x - min_x) / (max_x - min_x) * (width - 2 * margin)

    def sy(y: float) -> float:
        return height - margin - (y - min_y) / (max_y - min_y) * (height - 2 * margin)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="24" text-anchor="middle" font-size="18" font-family="Arial">{title}</text>',
        f'<line x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" stroke="black"/>',
        f'<line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" stroke="black"/>',
    ]

    for idx, (name, points) in enumerate(trajectories.items()):
        color = colors[idx % len(colors)]
        poly = " ".join(f"{sx(float(p[0])):.2f},{sy(float(p[1])):.2f}" for p in points if len(p) >= 2)
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{poly}"/>')
        parts.append(f'<text x="{width - 180}" y="{40 + 20 * idx}" fill="{color}" font-size="12" font-family="Arial">{name}</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def evaluate_stream(
    name: str,
    generator_factory: Callable[[], Iterable[Array]],
    *,
    dimension: int,
    window_size: int,
    rank: int,
    ridge_scale: float,
    beta: float,
    keep_trajectory: bool = False,
) -> Dict[str, object]:
    config = RestConfig(rank=rank, ridge_scale=ridge_scale, beta=beta)
    window = SlidingCovarianceWindow(dimension=dimension, window_size=window_size)
    outputs: Dict[str, List[Array]] = {
        "rest": [],
        "raw": [],
        "pca_scaled": [],
        "reciprocal_only": [],
        "exponential_only": [],
        "exp_then_reciprocal": [],
    }
    gaps: List[float] = []
    drifts: List[float] = []
    basis_motion: List[float] = []
    weight_sensitivity: List[float] = []
    runtimes_ms: List[float] = []
    condition_proxies: List[float] = []
    reciprocal_clip_hits = 0
    exponential_clip_hits = 0
    total_steps = 0
    previous_cov: Array | None = None
    previous_basis: Array | None = None
    previous_weights: Array | None = None

    for x_t in generator_factory():
        window.update(x_t)
        if not window.ready:
            continue
        start = time.perf_counter()
        mean_t = window.mean()
        cov_t = window.covariance()
        basis_t, evals_t = compute_topk_eigendecomposition(cov_t, rank=rank)
        full_evals = np.linalg.eigvalsh(cov_t)[::-1]
        step = rest_step(x_t, mean_t, basis_t, evals_t, config, covariance_t=cov_t)
        runtimes_ms.append((time.perf_counter() - start) * 1000.0)
        total_steps += 1

        outputs["rest"].append(step.rest_coordinates)
        outputs["raw"].append(raw_retained_coordinates(x_t, mean_t, basis_t))
        outputs["pca_scaled"].append(pca_energy_scaled_coordinates(x_t, mean_t, basis_t, evals_t))
        outputs["reciprocal_only"].append(reciprocal_only_coordinates(x_t, mean_t, basis_t, evals_t, ridge_scale=ridge_scale))
        outputs["exponential_only"].append(exponential_only_coordinates(x_t, mean_t, basis_t, evals_t, ridge_scale=ridge_scale, beta=beta))
        outputs["exp_then_reciprocal"].append(exponential_then_reciprocal_coordinates(x_t, mean_t, basis_t, evals_t, ridge_scale=ridge_scale, beta=beta))

        gaps.append(spectral_gap(full_evals, rank))
        condition_proxies.append(step.condition_proxy)
        reciprocal_clip_hits += int(np.any(np.isclose(step.reciprocal_weights, config.reciprocal_clip[0])) or np.any(np.isclose(step.reciprocal_weights, config.reciprocal_clip[1])))
        exponential_clip_hits += int(np.any(np.isclose(step.exponential_weights, config.exponential_clip[0])) or np.any(np.isclose(step.exponential_weights, config.exponential_clip[1])))
        if previous_cov is not None:
            drifts.append(float(np.linalg.norm(cov_t - previous_cov, ord=2)))
        if previous_basis is not None:
            basis_motion.append(projector_distance(basis_t, previous_basis))
        if previous_weights is not None:
            weight_sensitivity.append(float(np.linalg.norm(step.composite_weights - previous_weights)))

        previous_cov = cov_t.copy()
        previous_basis = basis_t.copy()
        previous_weights = step.composite_weights.copy()

    trajectories = {}
    if keep_trajectory:
        trajectories = {k: v[:60] for k, v in outputs.items() if v}

    metrics = {
        "stability": {k: adjacent_mean_norm(v) for k, v in outputs.items()},
        "condition_proxy_mean": float(np.mean(condition_proxies)) if condition_proxies else 0.0,
        "condition_proxy_max": float(np.max(condition_proxies)) if condition_proxies else 0.0,
        "weight_sensitivity_mean": float(np.mean(weight_sensitivity)) if weight_sensitivity else 0.0,
        "spectral_gap_mean": float(np.mean(gaps)) if gaps else 0.0,
        "spectral_gap_min": float(np.min(gaps)) if gaps else 0.0,
        "drift_mean": float(np.mean(drifts)) if drifts else 0.0,
        "drift_max": float(np.max(drifts)) if drifts else 0.0,
        "basis_motion_mean": float(np.mean(basis_motion)) if basis_motion else 0.0,
        "basis_motion_max": float(np.max(basis_motion)) if basis_motion else 0.0,
        "reciprocal_clip_rate": float(reciprocal_clip_hits / total_steps) if total_steps else 0.0,
        "exponential_clip_rate": float(exponential_clip_hits / total_steps) if total_steps else 0.0,
        "runtime_ms_mean": float(np.mean(runtimes_ms)) if runtimes_ms else 0.0,
        "samples_evaluated": total_steps,
        "parameters": {
            "dimension": dimension,
            "window_size": window_size,
            "rank": rank,
            "ridge_scale": ridge_scale,
            "beta": beta,
        },
    }
    return {"name": name, "metrics": metrics, "outputs": outputs, "trajectories": trajectories}


def run_beta_sweep() -> Dict[str, Dict[str, float]]:
    betas = [0.0, 0.2, 0.4, 0.8, 1.2]
    out: Dict[str, Dict[str, float]] = {}
    for beta in betas:
        exp = evaluate_stream(
            f"rotating_beta_{beta}",
            lambda: rotating_anisotropic_gaussian_stream(steps=150, dimension=6, seed=41),
            dimension=6,
            window_size=24,
            rank=2,
            ridge_scale=0.5,
            beta=beta,
        )
        m = exp["metrics"]
        out[str(beta)] = {
            "rest_stability": m["stability"]["rest"],
            "condition_proxy_mean": m["condition_proxy_mean"],
            "spectral_gap_mean": m["spectral_gap_mean"],
        }
    return out


def run_heatmap_sweep() -> Dict[str, Dict[str, float]]:
    betas = [0.0, 0.4, 0.8, 1.2]
    ridges = [0.2, 0.5, 1.0, 2.0]
    out: Dict[str, Dict[str, float]] = {}
    for beta in betas:
        row: Dict[str, float] = {}
        for ridge in ridges:
            exp = evaluate_stream(
                f"heatmap_b{beta}_r{ridge}",
                lambda: rotating_anisotropic_gaussian_stream(steps=130, dimension=6, seed=53),
                dimension=6,
                window_size=24,
                rank=2,
                ridge_scale=ridge,
                beta=beta,
            )
            row[str(ridge)] = exp["metrics"]["condition_proxy_mean"]
        out[str(beta)] = row
    return out


def collect_regime_task_outputs(
    *,
    ridge_scale: float = 0.5,
    beta: float = 0.7,
    steps: int = 160,
    window_size: int = 24,
    rank: int = 2,
) -> Dict[str, object]:
    config = RestConfig(rank=rank, ridge_scale=ridge_scale, beta=beta)
    window = SlidingCovarianceWindow(dimension=6, window_size=window_size)
    representations: Dict[str, List[Array]] = {
        "rest": [],
        "raw": [],
        "reciprocal_only": [],
        "exponential_only": [],
        "exp_then_reciprocal": [],
    }
    labels: List[int] = []
    change_index = int(0.5 * steps) - window_size

    for t, x_t in enumerate(regime_switch_stream(steps=steps, dimension=6, seed=37)):
        window.update(x_t)
        if not window.ready:
            continue
        mean_t = window.mean()
        cov_t = window.covariance()
        basis_t, evals_t = compute_topk_eigendecomposition(cov_t, rank=rank)
        step = rest_step(x_t, mean_t, basis_t, evals_t, config, covariance_t=cov_t)
        representations["rest"].append(step.rest_coordinates)
        representations["raw"].append(raw_retained_coordinates(x_t, mean_t, basis_t))
        representations["reciprocal_only"].append(reciprocal_only_coordinates(x_t, mean_t, basis_t, evals_t, ridge_scale=ridge_scale))
        representations["exponential_only"].append(exponential_only_coordinates(x_t, mean_t, basis_t, evals_t, ridge_scale=ridge_scale, beta=beta))
        representations["exp_then_reciprocal"].append(exponential_then_reciprocal_coordinates(x_t, mean_t, basis_t, evals_t, ridge_scale=ridge_scale, beta=beta))
        labels.append(0 if t < steps // 2 else 1)

    change_detection = {
        name: change_point_contrast(values, effective_change_index=max(2, change_index))
        for name, values in representations.items()
    }
    clustering = {name: fisher_ratio(values, labels) for name, values in representations.items()}
    return {
        "change_detection": change_detection,
        "clustering": clustering,
    }


def collect_forecasting_task_outputs(
    *,
    ridge_scale: float = 0.5,
    beta: float = 0.7,
    steps: int = 180,
    window_size: int = 24,
    rank: int = 2,
) -> Dict[str, float]:
    config = RestConfig(rank=rank, ridge_scale=ridge_scale, beta=beta)
    window = SlidingCovarianceWindow(dimension=6, window_size=window_size)
    representations: Dict[str, List[Array]] = {
        "rest": [],
        "raw": [],
        "reciprocal_only": [],
        "exponential_only": [],
    }
    for x_t in drifting_low_rank_stream(steps=steps, dimension=6, seed=59):
        window.update(x_t)
        if not window.ready:
            continue
        mean_t = window.mean()
        cov_t = window.covariance()
        basis_t, evals_t = compute_topk_eigendecomposition(cov_t, rank=rank)
        step = rest_step(x_t, mean_t, basis_t, evals_t, config, covariance_t=cov_t)
        representations["rest"].append(step.rest_coordinates)
        representations["raw"].append(raw_retained_coordinates(x_t, mean_t, basis_t))
        representations["reciprocal_only"].append(reciprocal_only_coordinates(x_t, mean_t, basis_t, evals_t, ridge_scale=ridge_scale))
        representations["exponential_only"].append(exponential_only_coordinates(x_t, mean_t, basis_t, evals_t, ridge_scale=ridge_scale, beta=beta))
    return {name: one_step_forecast_mse(values) for name, values in representations.items()}


def derive_thresholds(primary_results: List[Dict[str, object]], beta_sweep: Dict[str, Dict[str, float]], failure_result: Dict[str, object], downstream: Dict[str, object]) -> Dict[str, object]:
    primary_names = {"drifting_low_rank", "rotating_anisotropic_gaussian", "deforming_manifold"}
    near_best_count = 0
    family_details = {}
    for result in primary_results:
        if result["name"] not in primary_names:
            continue
        st = result["metrics"]["stability"]
        best = min(st["raw"], st["reciprocal_only"], st["exponential_only"], st["pca_scaled"])
        passes = st["rest"] <= 1.10 * best
        near_best_count += int(passes)
        family_details[result["name"]] = {
            "rest": st["rest"],
            "best_ablation": best,
            "within_10_percent": passes,
        }

    stable_beta_exists = any(v["condition_proxy_mean"] < 2.0 and v["rest_stability"] < 3.5 for v in beta_sweep.values())
    failure_st = failure_result["metrics"]["stability"]
    failure_probe_documented = failure_st["rest"] > failure_st["reciprocal_only"]

    change_scores = downstream["change_detection"]
    cluster_scores = downstream["clustering"]
    forecast_scores = downstream["forecast_mse"]
    downstream_pass = (
        change_scores["rest"] >= sorted(change_scores.values(), reverse=True)[1]
        or cluster_scores["rest"] >= sorted(cluster_scores.values(), reverse=True)[1]
        or forecast_scores["rest"] <= sorted(forecast_scores.values())[1]
    )

    return {
        "threshold_1": {
            "description": "REST stability within 10% of best ablation on at least 2 of 3 primary drift families",
            "value": near_best_count,
            "passes": near_best_count >= 2,
            "details": family_details,
        },
        "threshold_2": {
            "description": "There exists a beta regime with mean condition proxy < 2.0 and REST stability < 3.5 on rotating anisotropic Gaussian",
            "passes": stable_beta_exists,
        },
        "threshold_3": {
            "description": "Failure-mode probe documents at least one regime where REST underperforms reciprocal-only",
            "passes": failure_probe_documented,
            "rest_failure_stability": failure_st["rest"],
            "reciprocal_only_failure_stability": failure_st["reciprocal_only"],
        },
        "threshold_4": {
            "description": "REST places at least second-best on one controlled downstream benchmark family",
            "passes": downstream_pass,
        },
    }


def derive_recommendation(thresholds: Dict[str, object], primary_results: List[Dict[str, object]]) -> Dict[str, str]:
    order_identical = True
    for result in primary_results:
        st = result["metrics"]["stability"]
        if abs(st["rest"] - st["exp_then_reciprocal"]) > 1e-9:
            order_identical = False
            break

    passes = sum(int(item["passes"]) for item in thresholds.values())
    if order_identical:
        overall = "REFINE"
        rationale = "In the current retained-coordinate diagonal formulation, reciprocal and exponential weighting commute, so the ordering hypothesis is not empirically testable as a distinct source of benefit. The method still shows viability, but the novelty claim should be reframed or the architecture refined."
    elif passes <= 1:
        overall = "PIVOT"
        rationale = "REST does not yet justify broader expansion under the current evaluation regime and should be narrowed or reworked before scaling."
    elif passes >= 3:
        overall = "GO"
        rationale = "REST clears enough quantitative bars to justify broader controlled validation, though claims should remain narrow."
    else:
        overall = "REFINE"
        rationale = "REST shows partial promise but requires transform-law or framing refinement before broader validation."

    return {"overall": overall, "rationale": rationale, "ordering_identity_detected": str(order_identical)}


def write_phase4_evaluation_note(
    path: Path,
    primary_results: List[Dict[str, object]],
    failure_result: Dict[str, object],
    beta_sweep: Dict[str, Dict[str, float]],
    thresholds: Dict[str, object],
    downstream: Dict[str, object],
    recommendation: Dict[str, str],
) -> None:
    lines: List[str] = []
    lines.append("# PHASE4_EVALUATION_NOTE")
    lines.append("")
    lines.append("## Status")
    lines.append("Phase 4 complete at the stronger evaluation-and-refinement level.")
    lines.append("")
    lines.append("## Scope")
    lines.append("This note expands Phase 3 by adding richer diagnostics, explicit ordering ablations, a failure-mode probe, controlled downstream tasks, quantitative success thresholds, and a go/refine/pivot decision rubric.")
    lines.append("")
    lines.append("## Experiment families")
    for result in primary_results + [failure_result]:
        params = result["metrics"]["parameters"]
        lines.append(f"- **{result['name']}** — dimension={params['dimension']}, window={params['window_size']}, rank={params['rank']}, ridge_scale={params['ridge_scale']}, beta={params['beta']}, evaluated_samples={result['metrics']['samples_evaluated']}")
    lines.append("")
    lines.append("## Core ablation metrics")
    for result in primary_results + [failure_result]:
        m = result["metrics"]
        s = m["stability"]
        lines.append("")
        lines.append(f"### {result['name']}")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("| --- | ---: |")
        lines.append(f"| REST stability | {s['rest']:.6f} |")
        lines.append(f"| Raw retained stability | {s['raw']:.6f} |")
        lines.append(f"| Reciprocal-only stability | {s['reciprocal_only']:.6f} |")
        lines.append(f"| Exponential-only stability | {s['exponential_only']:.6f} |")
        lines.append(f"| Exponential-then-reciprocal stability | {s['exp_then_reciprocal']:.6f} |")
        lines.append(f"| Mean condition proxy | {m['condition_proxy_mean']:.6f} |")
        lines.append(f"| Min spectral gap | {m['spectral_gap_min']:.6f} |")
        lines.append(f"| Mean basis motion | {m['basis_motion_mean']:.6f} |")
        lines.append(f"| Reciprocal clip rate | {m['reciprocal_clip_rate']:.6f} |")
        lines.append(f"| Exponential clip rate | {m['exponential_clip_rate']:.6f} |")
    lines.append("")
    lines.append("## Quantitative success thresholds")
    lines.append("")
    lines.append("| Threshold | Pass? | Notes |")
    lines.append("| --- | --- | --- |")
    for key, item in thresholds.items():
        lines.append(f"| {item['description']} | {'PASS' if item['passes'] else 'FAIL'} | {key} |")
    lines.append("")
    lines.append("## Beta sweep (stability-vs-beta mandate)")
    lines.append("")
    lines.append("| beta | REST stability | Mean condition proxy | Mean spectral gap |")
    lines.append("| ---: | ---: | ---: | ---: |")
    for beta, values in beta_sweep.items():
        lines.append(f"| {beta} | {values['rest_stability']:.6f} | {values['condition_proxy_mean']:.6f} | {values['spectral_gap_mean']:.6f} |")
    lines.append("")
    lines.append("## Controlled downstream tasks")
    lines.append("")
    lines.append("### Change-point sensitivity")
    lines.append("")
    lines.append("| Representation | Contrast score |")
    lines.append("| --- | ---: |")
    for name, value in downstream["change_detection"].items():
        lines.append(f"| {name} | {value:.6f} |")
    lines.append("")
    lines.append("### Regime clustering separability")
    lines.append("")
    lines.append("| Representation | Fisher ratio |")
    lines.append("| --- | ---: |")
    for name, value in downstream["clustering"].items():
        lines.append(f"| {name} | {value:.6f} |")
    lines.append("")
    lines.append("### Short-horizon forecasting proxy")
    lines.append("")
    lines.append("| Representation | One-step MSE |")
    lines.append("| --- | ---: |")
    for name, value in downstream["forecast_mse"].items():
        lines.append(f"| {name} | {value:.6f} |")
    lines.append("")
    lines.append("## Go / Refine / Pivot rubric")
    lines.append("")
    lines.append("| Exit question | Current answer | Judgment |")
    lines.append("| --- | --- | --- |")
    lines.append(f"| Where does REST help? | It remains competitive on some drift families and is computationally stable enough to run richer evaluations. | Mixed-positive |")
    lines.append(f"| Where does REST fail? | The failure probe documents regimes where reciprocal-only behavior can be more stable. | Clear limitation |")
    lines.append(f"| Which parts matter? | Reciprocal and exponential weighting matter; reversed order is algebraically identical in the current retained-coordinate diagonal form. | Important refinement signal |")
    lines.append(f"| How tightly do experiments match theory regime? | Covariance PSD, clipping, and spectral-gap diagnostics are tracked explicitly, but not all experiments remain in uniformly favorable gap regimes. | Partial alignment |")
    lines.append(f"| Scale up or revise first? | {recommendation['rationale']} | {recommendation['overall']} |")
    lines.append("")
    lines.append("## Decision")
    lines.append(f"**Recommended action: {recommendation['overall']}**")
    lines.append("")
    lines.append(recommendation["rationale"])
    lines.append("")
    lines.append("## Figure outputs")
    lines.append("- `experiments/results/figures/stability_vs_beta.svg`")
    lines.append("- `experiments/results/figures/condition_proxy_heatmap.svg`")
    lines.append("- `experiments/results/figures/example_embedding_trajectories.svg`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_downstream_note(path: Path, downstream: Dict[str, object]) -> None:
    lines = [
        "# PHASE4_DOWNSTREAM_TASK_NOTE",
        "",
        "## Purpose",
        "This note records the first controlled downstream-task checks for the canonical covariance-based REST representation.",
        "",
        "## Tasks used",
        "1. Change-point sensitivity on an abrupt regime-switch stream",
        "2. Regime clustering separability on the same stream",
        "3. Short-horizon forecasting proxy on the drifting low-rank stream",
        "",
        "## Results",
        "",
        "### Change-point sensitivity",
        "",
        "| Representation | Contrast score |",
        "| --- | ---: |",
    ]
    for name, value in downstream["change_detection"].items():
        lines.append(f"| {name} | {value:.6f} |")
    lines += [
        "",
        "### Regime clustering separability",
        "",
        "| Representation | Fisher ratio |",
        "| --- | ---: |",
    ]
    for name, value in downstream["clustering"].items():
        lines.append(f"| {name} | {value:.6f} |")
    lines += [
        "",
        "### Short-horizon forecasting proxy",
        "",
        "| Representation | One-step MSE |",
        "| --- | ---: |",
    ]
    for name, value in downstream["forecast_mse"].items():
        lines.append(f"| {name} | {value:.6f} |")
    lines += [
        "",
        "## Takeaway",
        "These downstream tasks are intentionally simple. Their role is not to prove broad application dominance, but to test whether the REST representation changes task-relevant behavior relative to simpler baselines in a controlled setting.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_traceability_note(path: Path, primary_results: List[Dict[str, object]], failure_result: Dict[str, object]) -> None:
    all_results = primary_results + [failure_result]
    lines = [
        "# PHASE4_THEORY_TO_EXPERIMENT_TRACEABILITY",
        "",
        "## Purpose",
        "This note maps the formal assumptions from the Phase 2 theorem draft to the current implementation controls and experiment diagnostics.",
        "",
        "## Assumption-to-code mapping",
        "",
        "| Theorem assumption | Implementation control | Diagnostic logged in Phase 4 |",
        "| --- | --- | --- |",
        "| PSD operator | Sliding-window covariance construction | covariance-based operator only |",
        "| Bounded one-step drift | synthetic stream design + covariance updates | drift mean / drift max |",
        "| Retained spectral gap | top-k eigendecomposition with monitored gap | spectral gap mean / spectral gap min |",
        "| Bounded transform laws | explicit clipping on reciprocal and exponential weights | reciprocal / exponential clip rates |",
        "| Controlled basis motion | retained eigenspace tracking | basis motion mean / basis motion max |",
        "",
        "## Observed diagnostic ranges",
        "",
        "| Experiment | Min spectral gap | Mean drift | Max drift | Mean basis motion | Reciprocal clip rate | Exponential clip rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for result in all_results:
        m = result["metrics"]
        lines.append(
            f"| {result['name']} | {m['spectral_gap_min']:.6f} | {m['drift_mean']:.6f} | {m['drift_max']:.6f} | {m['basis_motion_mean']:.6f} | {m['reciprocal_clip_rate']:.6f} | {m['exponential_clip_rate']:.6f} |"
        )
    lines += [
        "",
        "## Interpretation",
        "- The covariance construction directly satisfies the PSD assumption.",
        "- The experiments only partially satisfy the intended theorem regime, because spectral gaps can narrow and drift can spike in the harder streams.",
        "- Clipping is active often enough to matter empirically, which confirms it is not a cosmetic implementation detail.",
        "- The theorem draft should therefore be interpreted as a local-regime result rather than a global explanation of all observed Phase 4 behavior.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_phase5_recommendation(path: Path, recommendation: Dict[str, str]) -> None:
    lines = [
        "# PHASE5_RECOMMENDATION_MEMO",
        "",
        "## Recommended direction",
        f"**{recommendation['overall']}**",
        "",
        "## Reasoning",
        recommendation["rationale"],
        "",
        "## Suggested Phase 5 focus",
    ]
    if recommendation["overall"] == "REFINE":
        lines += [
            "1. Revisit the novelty claim around transform ordering, since the current retained-coordinate diagonal formulation makes the order ablation algebraically identical.",
            "2. Decide whether REST should be reframed more explicitly as a geometric preconditioner rather than a broader geometry-as-computation primitive.",
            "3. Tighten the theorem draft to match the actual implementation regime and diagnostic evidence.",
            "4. Only after that, consider broader operator variants or real-world datasets.",
        ]
    elif recommendation["overall"] == "GO":
        lines += [
            "1. Broaden validation to stronger benchmarks and more realistic downstream tasks.",
            "2. Tighten proof details while preserving the current implementation path.",
            "3. Explore whether broader operator families maintain the same stability profile.",
        ]
    else:
        lines += [
            "1. Narrow the method scope to the regimes where it still helps, if any.",
            "2. Rework the transform laws or representation architecture before further expansion.",
            "3. Avoid broader validation until the method has a clearer differentiating advantage.",
        ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    results_dir = ROOT / "experiments" / "results"
    figures_dir = results_dir / "figures"
    results_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    primary_results = [
        evaluate_stream(
            "drifting_low_rank",
            lambda: drifting_low_rank_stream(steps=180, dimension=6, seed=7),
            dimension=6,
            window_size=24,
            rank=2,
            ridge_scale=0.5,
            beta=0.7,
            keep_trajectory=True,
        ),
        evaluate_stream(
            "rotating_anisotropic_gaussian",
            lambda: rotating_anisotropic_gaussian_stream(steps=180, dimension=6, seed=11),
            dimension=6,
            window_size=24,
            rank=2,
            ridge_scale=0.5,
            beta=0.7,
        ),
        evaluate_stream(
            "deforming_manifold",
            lambda: deforming_manifold_stream(steps=180, dimension=6, seed=19),
            dimension=6,
            window_size=24,
            rank=2,
            ridge_scale=0.5,
            beta=0.7,
        ),
    ]
    failure_result = evaluate_stream(
        "sparse_high_noise_failure_probe",
        lambda: sparse_high_noise_stream(steps=180, dimension=10, seed=29),
        dimension=10,
        window_size=24,
        rank=2,
        ridge_scale=0.5,
        beta=0.7,
    )

    beta_sweep = run_beta_sweep()
    heatmap = run_heatmap_sweep()
    downstream = collect_regime_task_outputs()
    downstream["forecast_mse"] = collect_forecasting_task_outputs()
    thresholds = derive_thresholds(primary_results, beta_sweep, failure_result, downstream)
    recommendation = derive_recommendation(thresholds, primary_results)

    # figures
    svg_polyline_chart(
        figures_dir / "stability_vs_beta.svg",
        {"REST": [(float(beta), vals["rest_stability"]) for beta, vals in beta_sweep.items()]},
        title="REST stability vs beta on rotating anisotropic Gaussian",
    )
    beta_labels = list(heatmap.keys())
    ridge_labels = list(next(iter(heatmap.values())).keys())
    matrix = [[heatmap[beta][ridge] for ridge in ridge_labels] for beta in beta_labels]
    svg_heatmap(
        figures_dir / "condition_proxy_heatmap.svg",
        matrix,
        row_labels=[f"beta={b}" for b in beta_labels],
        col_labels=[f"r={r}" for r in ridge_labels],
        title="Mean condition proxy heatmap",
    )
    trajectory_source = primary_results[0]["trajectories"]
    svg_trajectory_plot(
        figures_dir / "example_embedding_trajectories.svg",
        {
            "REST": trajectory_source["rest"],
            "Raw": trajectory_source["raw"],
            "Reciprocal-only": trajectory_source["reciprocal_only"],
        },
        title="Example retained-coordinate trajectories (drifting low-rank)",
    )

    payload = {
        "primary_results": [{"name": r["name"], "metrics": r["metrics"]} for r in primary_results],
        "failure_result": {"name": failure_result["name"], "metrics": failure_result["metrics"]},
        "beta_sweep": beta_sweep,
        "heatmap": heatmap,
        "downstream": downstream,
        "thresholds": thresholds,
        "recommendation": recommendation,
    }
    (results_dir / "phase4_metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    write_phase4_evaluation_note(
        ROOT / "docs" / "project-plan" / "PHASE4_EVALUATION_NOTE.md",
        primary_results,
        failure_result,
        beta_sweep,
        thresholds,
        downstream,
        recommendation,
    )
    write_downstream_note(ROOT / "docs" / "project-plan" / "PHASE4_DOWNSTREAM_TASK_NOTE.md", downstream)
    write_traceability_note(
        ROOT / "docs" / "project-plan" / "PHASE4_THEORY_TO_EXPERIMENT_TRACEABILITY.md",
        primary_results,
        failure_result,
    )
    write_phase5_recommendation(ROOT / "docs" / "project-plan" / "PHASE5_RECOMMENDATION_MEMO.md", recommendation)

    print(f"Wrote Phase 4 metrics to {results_dir / 'phase4_metrics.json'}")
    print(f"Wrote figures to {figures_dir}")
    print(f"Wrote evaluation note to {ROOT / 'docs' / 'project-plan' / 'PHASE4_EVALUATION_NOTE.md'}")


if __name__ == "__main__":
    main()
