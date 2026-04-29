from __future__ import annotations

import json
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from baselines.covariance import raw_retained_coordinates, reciprocal_only_coordinates  # noqa: E402
from rest.core import RestConfig, SlidingCovarianceWindow, compute_topk_eigendecomposition, rest_step  # noqa: E402

Array = np.ndarray
EPS = 1e-12


@dataclass(frozen=True)
class DecisionSliceConfig:
    steps: int = 220
    dimension: int = 6
    window_size: int = 28
    rank: int = 2
    ridge_scale: float = 0.5
    beta: float = 0.7
    rotation_speed: float = 0.035
    latent_persistence: float = 0.82
    latent_noise: float = 0.55
    observation_noise: float = 0.05


@dataclass(frozen=True)
class RegimeConfig:
    name: str
    description: str
    major_scale: float
    minor_scale: float


REGIMES: Tuple[RegimeConfig, ...] = (
    RegimeConfig(
        name="clean_gap",
        description="moderate drift with a clear dominant spectral direction",
        major_scale=3.0,
        minor_scale=0.45,
    ),
    RegimeConfig(
        name="medium_gap",
        description="moderate drift with a present but less dominant spectral gap",
        major_scale=2.1,
        minor_scale=0.9,
    ),
    RegimeConfig(
        name="messy_gap",
        description="moderate drift with weak / messy top-two separation",
        major_scale=1.45,
        minor_scale=1.15,
    ),
)

METHODS: Tuple[str, ...] = ("rest", "reciprocal_only", "covariance_whitening", "no_transform")
SEEDS: Tuple[int, ...] = (101, 202, 303, 404, 505)


def rotation_matrix(theta: float) -> Array:
    c = float(np.cos(theta))
    s = float(np.sin(theta))
    return np.array([[c, -s], [s, c]], dtype=float)


def generate_moderate_drift_regime(
    regime: RegimeConfig,
    *,
    config: DecisionSliceConfig,
    seed: int,
) -> Tuple[Array, Array]:
    """Generate a controlled moderate-drift stream plus next-step scalar targets.

    The target is the next latent primary coordinate. This keeps the downstream task
    common across all representations while stressing whether a transform preserves
    predictive signal under rotating anisotropic covariance.
    """

    rng = np.random.default_rng(seed)
    latent = np.zeros((config.steps + 1, 2), dtype=float)
    latent[0] = rng.normal(size=2)
    for t in range(1, config.steps + 1):
        latent[t] = (
            config.latent_persistence * latent[t - 1]
            + rng.normal(scale=config.latent_noise, size=2)
        )

    points = np.zeros((config.steps, config.dimension), dtype=float)
    scales = np.array([regime.major_scale, regime.minor_scale], dtype=float)
    for t in range(config.steps):
        rot = rotation_matrix(config.rotation_speed * t)
        signal2 = rot @ (scales * latent[t])
        points[t, :2] = signal2
        if config.dimension > 2:
            points[t, 2:] = rng.normal(scale=config.observation_noise, size=config.dimension - 2)
        points[t] += rng.normal(scale=config.observation_noise, size=config.dimension)

    # Feature at t predicts the primary latent coordinate at t+1.
    targets = latent[1 : config.steps + 1, 0]
    return points, targets


def covariance_whitening_coordinates(
    x_t: Array,
    mean_t: Array,
    basis_t: Array,
    eigenvalues_t: Array,
    ridge_scale: float,
) -> Array:
    coords = raw_retained_coordinates(x_t, mean_t, basis_t)
    # Classic retained-coordinate whitening, intentionally unclipped and with a tiny
    # numerical floor. This is a simple whitening baseline distinct from the clipped
    # reciprocal-only transform used by REST's reciprocal component.
    floor = max(EPS, ridge_scale * 1e-6)
    return coords / np.sqrt(np.maximum(eigenvalues_t, floor))


def adjacent_mean_norm(vectors: List[Array]) -> float:
    if len(vectors) < 2:
        return 0.0
    return float(np.mean([np.linalg.norm(vectors[i] - vectors[i - 1]) for i in range(1, len(vectors))]))


def temporal_regression_mse(features: List[Array], targets: List[float]) -> float:
    if len(features) < 12:
        return float("nan")
    x = np.vstack(features)
    y = np.asarray(targets, dtype=float)
    split = max(8, int(0.7 * len(x)))
    x_train, x_test = x[:split], x[split:]
    y_train, y_test = y[:split], y[split:]
    if len(x_test) == 0:
        return float("nan")

    # Intercept + tiny ridge for stable temporal regression.
    x_train_i = np.column_stack([np.ones(len(x_train)), x_train])
    x_test_i = np.column_stack([np.ones(len(x_test)), x_test])
    ridge = 1e-6 * np.eye(x_train_i.shape[1])
    ridge[0, 0] = 0.0
    coef = np.linalg.solve(x_train_i.T @ x_train_i + ridge, x_train_i.T @ y_train)
    pred = x_test_i @ coef
    return float(np.mean((pred - y_test) ** 2))


def evaluate_regime_seed(
    regime: RegimeConfig,
    *,
    config: DecisionSliceConfig,
    seed: int,
) -> Dict[str, object]:
    points, targets = generate_moderate_drift_regime(regime, config=config, seed=seed)
    rest_config = RestConfig(rank=config.rank, ridge_scale=config.ridge_scale, beta=config.beta)
    window = SlidingCovarianceWindow(dimension=config.dimension, window_size=config.window_size)

    representations: Dict[str, List[Array]] = {method: [] for method in METHODS}
    target_values: List[float] = []
    transform_times: Dict[str, List[float]] = {method: [] for method in METHODS}
    spectral_gaps: List[float] = []
    condition_proxies: List[float] = []

    for t, x_t in enumerate(points):
        window.update(x_t)
        if not window.ready:
            continue

        mean_t = window.mean()
        cov_t = window.covariance()
        basis_t, evals_t = compute_topk_eigendecomposition(cov_t, rank=config.rank)
        full_evals = np.linalg.eigvalsh(cov_t)[::-1]
        if config.rank < len(full_evals):
            spectral_gaps.append(float(full_evals[config.rank - 1] - full_evals[config.rank]))
        else:
            spectral_gaps.append(float(full_evals[config.rank - 1]))

        start = time.perf_counter()
        step = rest_step(x_t, mean_t, basis_t, evals_t, rest_config, covariance_t=cov_t)
        transform_times["rest"].append((time.perf_counter() - start) * 1000.0)
        representations["rest"].append(step.rest_coordinates)
        condition_proxies.append(step.condition_proxy)

        start = time.perf_counter()
        representations["reciprocal_only"].append(
            reciprocal_only_coordinates(
                x_t,
                mean_t,
                basis_t,
                evals_t,
                ridge_scale=config.ridge_scale,
                reciprocal_clip=rest_config.reciprocal_clip,
            )
        )
        transform_times["reciprocal_only"].append((time.perf_counter() - start) * 1000.0)

        start = time.perf_counter()
        representations["covariance_whitening"].append(
            covariance_whitening_coordinates(x_t, mean_t, basis_t, evals_t, config.ridge_scale)
        )
        transform_times["covariance_whitening"].append((time.perf_counter() - start) * 1000.0)

        start = time.perf_counter()
        representations["no_transform"].append(raw_retained_coordinates(x_t, mean_t, basis_t))
        transform_times["no_transform"].append((time.perf_counter() - start) * 1000.0)

        target_values.append(float(targets[t]))

    method_metrics = {}
    for method, values in representations.items():
        method_metrics[method] = {
            "stability": adjacent_mean_norm(values),
            "downstream_error": temporal_regression_mse(values, target_values),
            "runtime_ms_mean": float(np.mean(transform_times[method])) if transform_times[method] else 0.0,
        }

    return {
        "regime": regime.name,
        "seed": seed,
        "samples_evaluated": len(target_values),
        "spectral_gap_mean": float(np.mean(spectral_gaps)) if spectral_gaps else 0.0,
        "spectral_gap_min": float(np.min(spectral_gaps)) if spectral_gaps else 0.0,
        "condition_proxy_mean": float(np.mean(condition_proxies)) if condition_proxies else 0.0,
        "methods": method_metrics,
    }


def aggregate_regime(regime: RegimeConfig, seed_results: List[Dict[str, object]]) -> Dict[str, object]:
    aggregate_methods: Dict[str, Dict[str, float]] = {}
    for method in METHODS:
        stability = np.array([r["methods"][method]["stability"] for r in seed_results], dtype=float)
        error = np.array([r["methods"][method]["downstream_error"] for r in seed_results], dtype=float)
        runtime = np.array([r["methods"][method]["runtime_ms_mean"] for r in seed_results], dtype=float)
        aggregate_methods[method] = {
            "stability_mean": float(np.mean(stability)),
            "stability_seed_variance": float(np.var(stability, ddof=0)),
            "downstream_error_mean": float(np.mean(error)),
            "downstream_error_seed_variance": float(np.var(error, ddof=0)),
            "runtime_ms_mean": float(np.mean(runtime)),
            "runtime_ms_seed_variance": float(np.var(runtime, ddof=0)),
        }

    rest = aggregate_methods["rest"]
    reciprocal = aggregate_methods["reciprocal_only"]
    runtime_ok = rest["runtime_ms_mean"] <= 3.0 * max(reciprocal["runtime_ms_mean"], EPS)
    rest_error_ratio = rest["downstream_error_mean"] / max(reciprocal["downstream_error_mean"], EPS)
    rest_stability_ratio = rest["stability_mean"] / max(reciprocal["stability_mean"], EPS)

    if rest_error_ratio <= 0.95 and rest_stability_ratio <= 1.10 and runtime_ok:
        interpretation = "useful"
    elif rest_error_ratio <= 1.05 or rest_stability_ratio <= 1.05:
        interpretation = "neutral"
    else:
        interpretation = "negative"

    return {
        "name": regime.name,
        "description": regime.description,
        "seeds": [r["seed"] for r in seed_results],
        "samples_evaluated_per_seed": [r["samples_evaluated"] for r in seed_results],
        "spectral_gap_mean": float(np.mean([r["spectral_gap_mean"] for r in seed_results])),
        "spectral_gap_min": float(np.min([r["spectral_gap_min"] for r in seed_results])),
        "condition_proxy_mean": float(np.mean([r["condition_proxy_mean"] for r in seed_results])),
        "methods": aggregate_methods,
        "scorecard": {
            "rest_vs_reciprocal_downstream_error_ratio": float(rest_error_ratio),
            "rest_vs_reciprocal_stability_ratio": float(rest_stability_ratio),
            "runtime_ok_vs_reciprocal": bool(runtime_ok),
            "interpretation": interpretation,
        },
    }


def derive_overall_decision(regime_summaries: List[Dict[str, object]]) -> Dict[str, str]:
    interpretations = [r["scorecard"]["interpretation"] for r in regime_summaries]
    useful = interpretations.count("useful")
    negative = interpretations.count("negative")
    reciprocal_matches_or_beats_all = all(
        r["scorecard"]["rest_vs_reciprocal_downstream_error_ratio"] >= 0.98
        and r["scorecard"]["rest_vs_reciprocal_stability_ratio"] >= 0.98
        for r in regime_summaries
    )

    if useful >= 1:
        decision = "CONTINUE"
        rationale = "REST wins clearly on at least one locked moderate-drift spectral-gap regime without losing the runtime check."
    elif reciprocal_matches_or_beats_all:
        decision = "PIVOT"
        rationale = "Reciprocal-only matches or beats REST across the locked regimes on both downstream error and stability, so the current architecture does not earn mainline continuation from this slice."
    elif negative >= 2:
        decision = "PIVOT"
        rationale = "REST is negative in most locked regimes relative to reciprocal-only, so the current architecture should not be broadened before revision."
    else:
        decision = "REFINE"
        rationale = "Results are mixed or near-tie rather than a clean win; there may be a narrow niche, but the current architecture needs targeted refinement before expansion."

    return {"decision": decision, "rationale": rationale}


def run_decision_slice(
    *,
    config: DecisionSliceConfig = DecisionSliceConfig(),
    regimes: Iterable[RegimeConfig] = REGIMES,
    seeds: Iterable[int] = SEEDS,
) -> Dict[str, object]:
    regime_summaries = []
    raw_runs = []
    for regime in regimes:
        seed_results = [evaluate_regime_seed(regime, config=config, seed=seed) for seed in seeds]
        raw_runs.extend(seed_results)
        regime_summaries.append(aggregate_regime(regime, seed_results))

    decision = derive_overall_decision(regime_summaries)
    return {
        "schema_version": "decision-slice-v1",
        "locked_target": {
            "target_regime": "moderate-drift synthetic streams with clean-to-messy spectral-gap variation",
            "primary_question": "Does REST retain an edge once reciprocal-only is included seriously?",
            "downstream_task": "short-horizon online regression plus stability scorecard",
            "baselines": list(METHODS),
            "primary_metrics": ["stability", "downstream_error", "seed_variance", "runtime"],
        },
        "config": asdict(config),
        "seeds": list(seeds),
        "regimes": regime_summaries,
        "raw_runs": raw_runs,
        "overall_decision": decision,
        "post_pivot_claim_control": {
            "hard_baseline": "reciprocal_only",
            "protocol": "docs/project-plan/POST_PIVOT_REFINEMENT_PROTOCOL_2026-04-28.md",
            "current_rest_status": "reference_implementation_not_validated_continuation",
            "rule": "Stop or refine if reciprocal-only remains enough; no theorem prose in place of benchmark evidence.",
        },
    }


def format_float(value: float) -> str:
    return f"{value:.6f}"


def write_evaluation_note(path: Path, payload: Dict[str, object]) -> None:
    lines: List[str] = []
    lines.append("# CHAIRMAN_DECISION_SLICE_EVALUATION_NOTE_2026-04-28")
    lines.append("")
    lines.append("## Status")
    lines.append("Locked DOG decision slice executed.")
    lines.append("")
    lines.append("## Locked question")
    lines.append("> Does REST retain a defendable edge in moderate-drift synthetic streams with clean-to-messy spectral-gap variation once reciprocal-only is treated as a serious baseline?")
    lines.append("")
    lines.append("## Benchmark harness")
    lines.append("- Script: `experiments/synthetic/run_decision_slice.py`")
    lines.append("- Metrics JSON: `experiments/results/decision_slice_metrics.json`")
    lines.append("- Regimes: clean_gap, medium_gap, messy_gap")
    lines.append("- Baselines: REST, reciprocal-only, covariance-whitening, no-transform")
    lines.append("- Task: temporal short-horizon regression from each representation to the next primary latent coordinate")
    lines.append("")
    lines.append("## Scorecard schema")
    lines.append("Each regime records:")
    lines.append("- stability mean and seed variance,")
    lines.append("- downstream regression error mean and seed variance,")
    lines.append("- transform runtime mean and seed variance,")
    lines.append("- REST-vs-reciprocal downstream-error ratio,")
    lines.append("- REST-vs-reciprocal stability ratio,")
    lines.append("- useful / neutral / negative interpretation.")
    lines.append("")
    lines.append("## Regime results")
    for regime in payload["regimes"]:
        lines.append("")
        lines.append(f"### {regime['name']}")
        lines.append(regime["description"])
        lines.append("")
        lines.append(f"- mean spectral gap: {format_float(regime['spectral_gap_mean'])}")
        lines.append(f"- minimum spectral gap: {format_float(regime['spectral_gap_min'])}")
        lines.append(f"- mean REST condition proxy: {format_float(regime['condition_proxy_mean'])}")
        lines.append(f"- scorecard interpretation: **{regime['scorecard']['interpretation'].upper()}**")
        lines.append(f"- REST / reciprocal downstream-error ratio: {format_float(regime['scorecard']['rest_vs_reciprocal_downstream_error_ratio'])}")
        lines.append(f"- REST / reciprocal stability ratio: {format_float(regime['scorecard']['rest_vs_reciprocal_stability_ratio'])}")
        lines.append("")
        lines.append("| Method | Stability mean | Stability seed var | Downstream error mean | Downstream error seed var | Runtime ms mean |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
        for method, metrics in regime["methods"].items():
            lines.append(
                f"| {method} | {format_float(metrics['stability_mean'])} | {format_float(metrics['stability_seed_variance'])} | {format_float(metrics['downstream_error_mean'])} | {format_float(metrics['downstream_error_seed_variance'])} | {format_float(metrics['runtime_ms_mean'])} |"
            )
    lines.append("")
    decision = payload["overall_decision"]
    lines.append("## Continue / Refine / Pivot decision")
    lines.append(f"**Decision: {decision['decision']}**")
    lines.append("")
    lines.append(decision["rationale"])
    lines.append("")
    lines.append("## Interpretation")
    if decision["decision"] == "CONTINUE":
        lines.append("The current REST architecture earned at least one concrete niche in the locked slice. The next work should deepen that regime rather than broaden indiscriminately.")
    elif decision["decision"] == "REFINE":
        lines.append("The slice does not justify broad expansion. It supports targeted refinement and a tighter account of where REST differs from simpler reciprocal conditioning.")
    else:
        lines.append("The locked slice does not support continuing the current REST architecture as-is. Reciprocal-only is too competitive, so the next strategic step should be bounded architectural revision or scope demotion rather than broader validation.")
    lines.append("")
    lines.append("## Post-PIVOT claim control")
    lines.append("- Current REST status: reference implementation, not validated continuation.")
    lines.append("- Hard baseline for next slices: reciprocal-only.")
    lines.append("- Protocol: `docs/project-plan/POST_PIVOT_REFINEMENT_PROTOCOL_2026-04-28.md`.")
    lines.append("- Stop/refine if reciprocal-only remains enough.")
    lines.append("- Do not use theorem prose as a substitute for benchmark evidence.")
    lines.append("")
    lines.append("## Command")
    lines.append("```bash")
    lines.append("PYTHONPATH=src .venv/bin/python experiments/synthetic/run_decision_slice.py")
    lines.append("```")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    results_dir = ROOT / "experiments" / "results"
    docs_dir = ROOT / "docs" / "project-plan"
    results_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    payload = run_decision_slice()
    metrics_path = results_dir / "decision_slice_metrics.json"
    note_path = docs_dir / "CHAIRMAN_DECISION_SLICE_EVALUATION_NOTE_2026-04-28.md"
    metrics_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_evaluation_note(note_path, payload)

    decision = payload["overall_decision"]["decision"]
    print(f"Wrote {metrics_path}")
    print(f"Wrote {note_path}")
    print(f"Decision: {decision}")


if __name__ == "__main__":
    main()
