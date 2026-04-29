from __future__ import annotations

import json
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from baselines.covariance import raw_retained_coordinates, reciprocal_only_coordinates  # noqa: E402
from rest.core import RestConfig, SlidingCovarianceWindow, compute_topk_eigendecomposition, rest_step  # noqa: E402
from run_decision_slice import format_float  # noqa: E402
from run_prism_contract_mock import METHODS as PRISM_METHODS, PrismMockConfig, evaluate_mock_trace  # noqa: E402
from run_reciprocal_robustness_sweep import (  # noqa: E402
    AUDITABILITY_TOLERANCE,
    FALSE_PASS_TOLERANCE,
    RUNTIME_GUARDRAIL,
    STABILITY_GUARDRAIL,
    ratio,
)

Array = np.ndarray
EPS = 1e-12
METHODS: Tuple[str, ...] = ("rest", "reciprocal_only", "covariance_whitening", "no_transform")
SEEDS: Tuple[int, ...] = (111, 222, 333, 444, 555)

PROMISING_ERROR_RATIO = 0.98
RECIPROCAL_ABSOLUTE_NMSE_FAIL = 1.00
RECIPROCAL_RELATIVE_ERROR_FAIL = 1.10
RECIPROCAL_RELATIVE_STABILITY_FAIL = 1.25
RECIPROCAL_ABSOLUTE_STABILITY_FAIL = 1.50


@dataclass(frozen=True)
class AdversarialConfig:
    steps: int = 240
    dimension: int = 6
    window_size: int = 20
    rank: int = 2
    ridge_scale: float = 0.5
    beta: float = 0.7
    latent_persistence: float = 0.72
    latent_noise: float = 0.65
    observation_noise: float = 0.06


@dataclass(frozen=True)
class AdversarialCase:
    name: str
    description: str
    generator: str
    config: AdversarialConfig = AdversarialConfig()


def rotation(theta: float, dim: int = 2) -> Array:
    c = float(np.cos(theta))
    s = float(np.sin(theta))
    r = np.eye(dim)
    r[:2, :2] = np.array([[c, -s], [s, c]], dtype=float)
    return r


def latent_series(config: AdversarialConfig, rng: np.random.Generator, dims: int = 3) -> Array:
    latent = np.zeros((config.steps + 1, dims), dtype=float)
    latent[0] = rng.normal(size=dims)
    for t in range(1, config.steps + 1):
        latent[t] = config.latent_persistence * latent[t - 1] + rng.normal(scale=config.latent_noise, size=dims)
    return latent


def generate_switching_lag(config: AdversarialConfig, seed: int) -> Tuple[Array, Array]:
    rng = np.random.default_rng(seed)
    latent = latent_series(config, rng, dims=2)
    points = np.zeros((config.steps, config.dimension), dtype=float)
    for t in range(config.steps):
        block = (t // 32) % 2
        theta = (0.15 if block else -0.11) * t + (np.pi / 3 if block else 0.0)
        scales = np.array([3.4, 0.24], dtype=float) if not block else np.array([0.34, 2.9], dtype=float)
        signal = rotation(theta) @ (scales * latent[t])
        points[t, :2] = signal
        points[t, 2:] = rng.normal(scale=config.observation_noise, size=config.dimension - 2)
        points[t] += rng.normal(scale=config.observation_noise, size=config.dimension)
    return points, latent[1:, 0]


def generate_outlier_bursts(config: AdversarialConfig, seed: int) -> Tuple[Array, Array]:
    rng = np.random.default_rng(seed)
    latent = latent_series(config, rng, dims=2)
    points = np.zeros((config.steps, config.dimension), dtype=float)
    for t in range(config.steps):
        theta = 0.045 * t
        signal = rotation(theta) @ (np.array([2.0, 0.7]) * latent[t])
        points[t, :2] = signal
        points[t, 2:] = rng.normal(scale=config.observation_noise, size=config.dimension - 2)
        if t % 29 in (0, 1):
            points[t, 0] += rng.choice([-1.0, 1.0]) * rng.uniform(7.0, 10.0)
            points[t, 1] += rng.choice([-1.0, 1.0]) * rng.uniform(2.0, 4.0)
        points[t] += rng.normal(scale=config.observation_noise, size=config.dimension)
    return points, latent[1:, 0]


def generate_low_variance_target(config: AdversarialConfig, seed: int) -> Tuple[Array, Array]:
    rng = np.random.default_rng(seed)
    latent = latent_series(config, rng, dims=3)
    points = np.zeros((config.steps, config.dimension), dtype=float)
    for t in range(config.steps):
        theta = 0.03 * t
        high_var = rotation(theta) @ (np.array([4.0, 2.8]) * latent[t, :2])
        points[t, :2] = high_var
        points[t, 2] = 0.20 * latent[t, 2]
        points[t, 3:] = rng.normal(scale=0.10, size=config.dimension - 3)
        points[t] += rng.normal(scale=config.observation_noise, size=config.dimension)
    # Target sits in a low-variance direction likely to be under-served by rank-two retained covariance.
    return points, latent[1:, 2]


def generate_eigenvalue_collapse(config: AdversarialConfig, seed: int) -> Tuple[Array, Array]:
    rng = np.random.default_rng(seed)
    latent = latent_series(config, rng, dims=2)
    points = np.zeros((config.steps, config.dimension), dtype=float)
    for t in range(config.steps):
        theta = 0.20 * t
        wobble = 0.20 * np.sin(t / 9.0)
        scales = np.array([1.05 + wobble, 1.00 - wobble], dtype=float)
        points[t, :2] = rotation(theta) @ (scales * latent[t])
        points[t, 2:] = rng.normal(scale=0.16, size=config.dimension - 2)
        points[t] += rng.normal(scale=config.observation_noise, size=config.dimension)
    return points, latent[1:, 0]


def generate_reciprocal_clip_stress(config: AdversarialConfig, seed: int) -> Tuple[Array, Array]:
    rng = np.random.default_rng(seed)
    latent = latent_series(config, rng, dims=2)
    points = np.zeros((config.steps, config.dimension), dtype=float)
    for t in range(config.steps):
        theta = 0.06 * t
        # Tiny retained eigenvalue plus moderate noise stresses reciprocal clipping.
        signal = rotation(theta) @ (np.array([2.7, 0.035]) * latent[t])
        points[t, :2] = signal
        points[t, 2:] = rng.normal(scale=0.20, size=config.dimension - 2)
        points[t] += rng.normal(scale=config.observation_noise, size=config.dimension)
    return points, latent[1:, 1]


GENERATORS: Dict[str, Callable[[AdversarialConfig, int], Tuple[Array, Array]]] = {
    "switching_lag": generate_switching_lag,
    "outlier_bursts": generate_outlier_bursts,
    "low_variance_target": generate_low_variance_target,
    "eigenvalue_collapse": generate_eigenvalue_collapse,
    "reciprocal_clip_stress": generate_reciprocal_clip_stress,
}

ADVERSARIAL_CASES: Tuple[AdversarialCase, ...] = (
    AdversarialCase("switching_lag", "abrupt covariance swaps that stress window lag", "switching_lag"),
    AdversarialCase("outlier_bursts", "rare high-magnitude bursts contaminate covariance estimates", "outlier_bursts"),
    AdversarialCase("low_variance_target", "predictive target lives in a low-variance direction", "low_variance_target"),
    AdversarialCase("eigenvalue_collapse", "near-isotropic retained spectrum with rapid basis rotation", "eigenvalue_collapse"),
    AdversarialCase("reciprocal_clip_stress", "tiny retained eigenvalue stresses reciprocal clipping", "reciprocal_clip_stress"),
)

PRISM_ADVERSARIAL_CASES: Tuple[Tuple[str, str, PrismMockConfig], ...] = (
    ("default_mock", "current paper/mock contract trace", PrismMockConfig()),
    ("high_noise_contract", "higher contract-feature noise", PrismMockConfig(noise_scale=0.10, seed=1201)),
    ("tiny_window_contract", "very short contract covariance window", PrismMockConfig(window_size=4, rank=2, seed=1302)),
    ("low_repeats_contract", "few repeats per contract case", PrismMockConfig(repeats_per_case=4, window_size=4, rank=2, noise_scale=0.08, seed=1403)),
)


def covariance_whitening_coordinates(x_t: Array, mean_t: Array, basis_t: Array, eigenvalues_t: Array, ridge_scale: float) -> Array:
    coords = raw_retained_coordinates(x_t, mean_t, basis_t)
    return coords / np.sqrt(np.maximum(eigenvalues_t, max(EPS, ridge_scale * 1e-6)))


def adjacent_mean_norm(vectors: List[Array]) -> float:
    if len(vectors) < 2:
        return 0.0
    return float(np.mean([np.linalg.norm(vectors[i] - vectors[i - 1]) for i in range(1, len(vectors))]))


def regression_metrics(features: List[Array], targets: List[float]) -> Dict[str, float]:
    x = np.vstack(features)
    y = np.asarray(targets, dtype=float)
    split = max(8, int(0.7 * len(x)))
    x_train, x_test = x[:split], x[split:]
    y_train, y_test = y[:split], y[split:]
    x_train_i = np.column_stack([np.ones(len(x_train)), x_train])
    x_test_i = np.column_stack([np.ones(len(x_test)), x_test])
    ridge = 1e-6 * np.eye(x_train_i.shape[1])
    ridge[0, 0] = 0.0
    coef = np.linalg.solve(x_train_i.T @ x_train_i + ridge, x_train_i.T @ y_train)
    pred = x_test_i @ coef
    mse = float(np.mean((pred - y_test) ** 2))
    baseline = float(np.mean((y_test - np.mean(y_train)) ** 2))
    return {"mse": mse, "normalized_mse": ratio(mse, baseline)}


def evaluate_case_seed(case: AdversarialCase, seed: int) -> Dict[str, object]:
    points, targets = GENERATORS[case.generator](case.config, seed)
    rest_config = RestConfig(rank=case.config.rank, ridge_scale=case.config.ridge_scale, beta=case.config.beta)
    window = SlidingCovarianceWindow(dimension=case.config.dimension, window_size=case.config.window_size)
    representations: Dict[str, List[Array]] = {method: [] for method in METHODS}
    target_values: List[float] = []
    transform_times: Dict[str, List[float]] = {method: [] for method in METHODS}

    for t, x_t in enumerate(points):
        window.update(x_t)
        if not window.ready:
            continue
        mean_t = window.mean()
        cov_t = window.covariance()
        basis_t, evals_t = compute_topk_eigendecomposition(cov_t, rank=case.config.rank)

        start = time.perf_counter()
        step = rest_step(x_t, mean_t, basis_t, evals_t, rest_config, covariance_t=cov_t)
        transform_times["rest"].append((time.perf_counter() - start) * 1000.0)
        representations["rest"].append(step.rest_coordinates)

        start = time.perf_counter()
        representations["reciprocal_only"].append(
            reciprocal_only_coordinates(x_t, mean_t, basis_t, evals_t, case.config.ridge_scale, rest_config.reciprocal_clip)
        )
        transform_times["reciprocal_only"].append((time.perf_counter() - start) * 1000.0)

        start = time.perf_counter()
        representations["covariance_whitening"].append(
            covariance_whitening_coordinates(x_t, mean_t, basis_t, evals_t, case.config.ridge_scale)
        )
        transform_times["covariance_whitening"].append((time.perf_counter() - start) * 1000.0)

        start = time.perf_counter()
        representations["no_transform"].append(raw_retained_coordinates(x_t, mean_t, basis_t))
        transform_times["no_transform"].append((time.perf_counter() - start) * 1000.0)
        target_values.append(float(targets[t]))

    methods: Dict[str, Dict[str, float]] = {}
    for method, vectors in representations.items():
        reg = regression_metrics(vectors, target_values)
        methods[method] = {
            "stability": adjacent_mean_norm(vectors),
            "downstream_error": reg["mse"],
            "downstream_normalized_mse": reg["normalized_mse"],
            "runtime_ms_mean": float(np.mean(transform_times[method])) if transform_times[method] else 0.0,
        }
    return {"case": case.name, "seed": seed, "samples_evaluated": len(target_values), "methods": methods}


def aggregate_case(case: AdversarialCase, seed_results: List[Dict[str, object]]) -> Dict[str, object]:
    methods: Dict[str, Dict[str, float]] = {}
    for method in METHODS:
        methods[method] = {
            "stability_mean": float(np.mean([r["methods"][method]["stability"] for r in seed_results])),
            "downstream_error_mean": float(np.mean([r["methods"][method]["downstream_error"] for r in seed_results])),
            "downstream_normalized_mse_mean": float(np.mean([r["methods"][method]["downstream_normalized_mse"] for r in seed_results])),
            "runtime_ms_mean": float(np.mean([r["methods"][method]["runtime_ms_mean"] for r in seed_results])),
        }
    reciprocal = methods["reciprocal_only"]
    best_error = min(m["downstream_error_mean"] for m in methods.values())
    best_stability = min(m["stability_mean"] for m in methods.values())
    reciprocal_failure = {
        "absolute_downstream_failure": bool(reciprocal["downstream_normalized_mse_mean"] > RECIPROCAL_ABSOLUTE_NMSE_FAIL),
        "relative_downstream_failure": bool(ratio(reciprocal["downstream_error_mean"], best_error) >= RECIPROCAL_RELATIVE_ERROR_FAIL),
        "absolute_stability_failure": bool(reciprocal["stability_mean"] > RECIPROCAL_ABSOLUTE_STABILITY_FAIL),
        "relative_stability_failure": bool(ratio(reciprocal["stability_mean"], best_stability) >= RECIPROCAL_RELATIVE_STABILITY_FAIL),
    }
    reciprocal_failure["any_failure"] = any(reciprocal_failure.values())

    comparisons: Dict[str, Dict[str, object]] = {}
    for method, metrics in methods.items():
        error_ratio = ratio(metrics["downstream_error_mean"], reciprocal["downstream_error_mean"])
        stability_ratio = ratio(metrics["stability_mean"], reciprocal["stability_mean"])
        runtime_ratio = ratio(metrics["runtime_ms_mean"], reciprocal["runtime_ms_mean"])
        comparisons[method] = {
            "downstream_error_ratio_vs_reciprocal": error_ratio,
            "stability_ratio_vs_reciprocal": stability_ratio,
            "runtime_ratio_vs_reciprocal": runtime_ratio,
            "beats_reciprocal_dog_side": bool(
                method != "reciprocal_only"
                and error_ratio <= PROMISING_ERROR_RATIO
                and stability_ratio <= STABILITY_GUARDRAIL
                and runtime_ratio <= RUNTIME_GUARDRAIL
            ),
        }

    return {
        "case": case.name,
        "description": case.description,
        "generator": case.generator,
        "config": asdict(case.config),
        "seeds": [r["seed"] for r in seed_results],
        "samples_evaluated_per_seed": [r["samples_evaluated"] for r in seed_results],
        "methods": methods,
        "reciprocal_failure": reciprocal_failure,
        "baseline_comparison": comparisons,
    }


def evaluate_prism_guardrails() -> Tuple[List[Dict[str, object]], Dict[str, Dict[str, object]], Dict[str, object]]:
    scenarios: List[Dict[str, object]] = []
    method_guardrails: Dict[str, Dict[str, object]] = {
        method: {
            "max_false_pass_delta_vs_reciprocal": -float("inf"),
            "max_auditability_delta_vs_reciprocal": -float("inf"),
            "guardrail_ok_all_scenarios": True,
        }
        for method in PRISM_METHODS
        if method != "reciprocal_only"
    }
    reciprocal_contract_failures: List[Dict[str, object]] = []
    for name, description, config in PRISM_ADVERSARIAL_CASES:
        payload = evaluate_mock_trace(config)
        reciprocal = payload["methods"]["reciprocal_only"]
        reciprocal_contract_failure = {
            "false_pass_failure": bool(reciprocal["false_pass_rate"] > FALSE_PASS_TOLERANCE),
            "auditability_failure": bool(reciprocal["auditability_reconstruction_error"] > 0.20),
            "contract_error_failure": bool(reciprocal["contract_classification_error"] > 0.25),
        }
        reciprocal_contract_failure["any_failure"] = any(reciprocal_contract_failure.values())
        if reciprocal_contract_failure["any_failure"]:
            reciprocal_contract_failures.append({"scenario": name, **reciprocal_contract_failure})
        comparisons: Dict[str, Dict[str, object]] = {}
        for method, metrics in payload["methods"].items():
            false_pass_delta = metrics["false_pass_rate"] - reciprocal["false_pass_rate"]
            auditability_delta = metrics["auditability_reconstruction_error"] - reciprocal["auditability_reconstruction_error"]
            guardrail_ok = bool(false_pass_delta <= FALSE_PASS_TOLERANCE and auditability_delta <= AUDITABILITY_TOLERANCE)
            comparisons[method] = {
                "false_pass_delta_vs_reciprocal": float(false_pass_delta),
                "auditability_delta_vs_reciprocal": float(auditability_delta),
                "guardrail_ok": guardrail_ok,
            }
            if method != "reciprocal_only":
                guard = method_guardrails[method]
                guard["max_false_pass_delta_vs_reciprocal"] = max(guard["max_false_pass_delta_vs_reciprocal"], float(false_pass_delta))
                guard["max_auditability_delta_vs_reciprocal"] = max(guard["max_auditability_delta_vs_reciprocal"], float(auditability_delta))
                guard["guardrail_ok_all_scenarios"] = bool(guard["guardrail_ok_all_scenarios"] and guardrail_ok)
        scenarios.append(
            {
                "scenario": name,
                "description": description,
                "config": asdict(config),
                "reciprocal_contract_failure": reciprocal_contract_failure,
                "methods": payload["methods"],
                "baseline_comparison": comparisons,
                "decision": payload["scorecard"]["decision"],
            }
        )
    reciprocal_contract_summary = {
        "failure_scenarios": reciprocal_contract_failures,
        "any_contract_failure": bool(reciprocal_contract_failures),
    }
    return scenarios, method_guardrails, reciprocal_contract_summary


def derive_decision(case_summaries: List[Dict[str, object]], prism_guardrails: Dict[str, Dict[str, object]], reciprocal_contract_summary: Dict[str, object]) -> Dict[str, object]:
    reciprocal_failure_cases = [s for s in case_summaries if s["reciprocal_failure"]["any_failure"]]
    dog_side_candidates: Dict[str, List[Dict[str, object]]] = {m: [] for m in METHODS if m != "reciprocal_only"}
    promising_candidates: Dict[str, List[Dict[str, object]]] = {m: [] for m in METHODS if m != "reciprocal_only"}
    for summary in case_summaries:
        for method, comparison in summary["baseline_comparison"].items():
            if method == "reciprocal_only" or not comparison["beats_reciprocal_dog_side"]:
                continue
            record = {
                "case": summary["case"],
                "downstream_error_ratio_vs_reciprocal": comparison["downstream_error_ratio_vs_reciprocal"],
                "stability_ratio_vs_reciprocal": comparison["stability_ratio_vs_reciprocal"],
                "runtime_ratio_vs_reciprocal": comparison["runtime_ratio_vs_reciprocal"],
            }
            dog_side_candidates[method].append(record)
            if prism_guardrails.get(method, {}).get("guardrail_ok_all_scenarios", False):
                promising_candidates[method].append(record)
    promising_candidates = {m: wins for m, wins in promising_candidates.items() if wins}

    if promising_candidates:
        decision = "PROMISING_FAILURE_NICHE_FOUND"
        rationale = "At least one non-reciprocal method beat reciprocal-only on the DOG adversarial scorecard and preserved PRISM mock false-pass/auditability guardrails. Treat only those cases as bounded follow-up candidates."
    elif reciprocal_failure_cases or reciprocal_contract_summary["any_contract_failure"]:
        decision = "FAILURES_FOUND_NO_DOG_RESCUE"
        rationale = "The search found reciprocal-only failure criteria, but no current DOG method beat reciprocal-only while preserving PRISM guardrails. Recommend stopping current REST rescue and refocusing on baseline characterization or a pre-registered new variant only."
    else:
        decision = "NO_FAILURE_NICHE_FOUND"
        rationale = "The narrow adversarial search did not find a reciprocal-only failure niche under the registered criteria. Recommend stopping/refocusing rather than trying to rescue REST."

    return {
        "decision": decision,
        "rationale": rationale,
        "reciprocal_failure_case_count": len(reciprocal_failure_cases),
        "reciprocal_failure_cases": [s["case"] for s in reciprocal_failure_cases],
        "reciprocal_contract_failures": reciprocal_contract_summary["failure_scenarios"],
        "dog_side_candidates": {m: wins for m, wins in dog_side_candidates.items() if wins},
        "promising_candidates": promising_candidates,
    }


def run_adversarial_search(cases: Iterable[AdversarialCase] = ADVERSARIAL_CASES, seeds: Iterable[int] = SEEDS) -> Dict[str, object]:
    case_summaries: List[Dict[str, object]] = []
    raw_runs: List[Dict[str, object]] = []
    for case in cases:
        seed_results = [evaluate_case_seed(case, seed) for seed in seeds]
        raw_runs.extend(seed_results)
        case_summaries.append(aggregate_case(case, seed_results))
    prism_scenarios, prism_guardrails, reciprocal_contract_summary = evaluate_prism_guardrails()
    decision = derive_decision(case_summaries, prism_guardrails, reciprocal_contract_summary)
    return {
        "schema_version": "reciprocal-adversarial-failure-search-v1",
        "mode": "synthetic_and_prism_paper_mock_only",
        "hard_baseline": "reciprocal_only",
        "claim_boundary": "No PRISM live-use claims; no attempt to rescue REST; promising requires DOG-side win plus PRISM false-pass/auditability guardrails.",
        "failure_criteria": {
            "reciprocal_absolute_normalized_mse_gt": RECIPROCAL_ABSOLUTE_NMSE_FAIL,
            "reciprocal_relative_error_ratio_to_best_ge": RECIPROCAL_RELATIVE_ERROR_FAIL,
            "reciprocal_absolute_stability_gt": RECIPROCAL_ABSOLUTE_STABILITY_FAIL,
            "reciprocal_relative_stability_ratio_to_best_ge": RECIPROCAL_RELATIVE_STABILITY_FAIL,
            "candidate_downstream_error_ratio_vs_reciprocal_max": PROMISING_ERROR_RATIO,
            "candidate_stability_ratio_vs_reciprocal_max": STABILITY_GUARDRAIL,
            "candidate_runtime_ratio_vs_reciprocal_max": RUNTIME_GUARDRAIL,
            "candidate_false_pass_delta_vs_reciprocal_max": FALSE_PASS_TOLERANCE,
            "candidate_auditability_delta_vs_reciprocal_max": AUDITABILITY_TOLERANCE,
        },
        "seeds": list(seeds),
        "cases": case_summaries,
        "raw_runs": raw_runs,
        "prism_scenarios": prism_scenarios,
        "prism_method_guardrails": prism_guardrails,
        "decision": decision,
    }


def write_note(path: Path, payload: Dict[str, object]) -> None:
    lines: List[str] = []
    lines.append("# Reciprocal-Only Adversarial Failure Search — 2026-04-28")
    lines.append("")
    lines.append("## Status")
    lines.append("Executed narrow adversarial search. Reciprocal-only remains the current winning baseline; this slice searches for its failures rather than trying to rescue REST.")
    lines.append("")
    lines.append("## Claim boundary")
    lines.append("Synthetic DOG evidence plus PRISM paper/mock guardrails only. No PRISM live-use claim. No theorem prose in place of benchmark evidence.")
    lines.append("")
    lines.append("## Registered failure criteria")
    lines.append("Reciprocal-only is flagged as failing a DOG adversarial case if it crosses any of:")
    lines.append(f"- normalized downstream MSE > `{RECIPROCAL_ABSOLUTE_NMSE_FAIL}`;")
    lines.append(f"- downstream error / best method error >= `{RECIPROCAL_RELATIVE_ERROR_FAIL}`;")
    lines.append(f"- stability > `{RECIPROCAL_ABSOLUTE_STABILITY_FAIL}`;")
    lines.append(f"- stability / best method stability >= `{RECIPROCAL_RELATIVE_STABILITY_FAIL}`.")
    lines.append("")
    lines.append("A DOG method is promising only if it beats reciprocal-only on downstream error, stability, and runtime while also preserving PRISM false-pass and auditability guardrails.")
    lines.append("")
    lines.append("## Coverage")
    lines.append(f"- DOG adversarial cases: `{len(payload['cases'])}`")
    lines.append(f"- Seeds per case: `{len(payload['seeds'])}`")
    lines.append(f"- PRISM paper/mock adversarial guardrail scenarios: `{len(payload['prism_scenarios'])}`")
    lines.append("")
    lines.append("## Decision")
    lines.append(f"**{payload['decision']['decision']}**")
    lines.append("")
    lines.append(payload["decision"]["rationale"])
    lines.append("")
    lines.append("## Reciprocal-only failure cases")
    if payload["decision"]["reciprocal_failure_cases"]:
        for case in payload["cases"]:
            if not case["reciprocal_failure"]["any_failure"]:
                continue
            rec = case["methods"]["reciprocal_only"]
            flags = [k for k, v in case["reciprocal_failure"].items() if k != "any_failure" and v]
            lines.append(
                f"- `{case['case']}`: flags `{', '.join(flags)}`; reciprocal normalized MSE `{format_float(rec['downstream_normalized_mse_mean'])}`, stability `{format_float(rec['stability_mean'])}`"
            )
    else:
        lines.append("None under the registered DOG criteria.")
    lines.append("")
    lines.append("## Promising DOG candidates")
    if payload["decision"]["promising_candidates"]:
        for method, candidates in payload["decision"]["promising_candidates"].items():
            lines.append(f"### {method}")
            for candidate in candidates:
                lines.append(
                    f"- `{candidate['case']}`: error ratio `{format_float(candidate['downstream_error_ratio_vs_reciprocal'])}`, stability ratio `{format_float(candidate['stability_ratio_vs_reciprocal'])}`, runtime ratio `{format_float(candidate['runtime_ratio_vs_reciprocal'])}`"
                )
    else:
        lines.append("None. No current REST/whitening/no-transform path earns a follow-up claim from this search.")
    lines.append("")
    lines.append("## Case scorecard")
    lines.append("| Case | Reciprocal failed? | Recip norm MSE | Recip stability | Best DOG-side candidate |")
    lines.append("| --- | ---: | ---: | ---: | --- |")
    for case in payload["cases"]:
        best_candidate = "none"
        for method, comparison in case["baseline_comparison"].items():
            if comparison["beats_reciprocal_dog_side"]:
                best_candidate = method
                break
        rec = case["methods"]["reciprocal_only"]
        lines.append(
            f"| {case['case']} | {str(case['reciprocal_failure']['any_failure']).lower()} | {format_float(rec['downstream_normalized_mse_mean'])} | {format_float(rec['stability_mean'])} | {best_candidate} |"
        )
    lines.append("")
    lines.append("## PRISM guardrail summary")
    lines.append("| Method | Guardrail OK all scenarios | Max false-pass delta | Max auditability delta |")
    lines.append("| --- | ---: | ---: | ---: |")
    for method, metrics in payload["prism_method_guardrails"].items():
        lines.append(
            f"| {method} | {str(metrics['guardrail_ok_all_scenarios']).lower()} | {format_float(metrics['max_false_pass_delta_vs_reciprocal'])} | {format_float(metrics['max_auditability_delta_vs_reciprocal'])} |"
        )
    lines.append("")
    lines.append("## Recommendation")
    if payload["decision"]["decision"] == "PROMISING_FAILURE_NICHE_FOUND":
        lines.append("Run a bounded follow-up only on the listed failure niche. Do not generalize beyond it.")
    else:
        lines.append("Stop trying to rescue current REST from this evidence. Refocus on reciprocal-only characterization, scope demotion, or a separately pre-registered new variant if one is genuinely motivated.")
    lines.append("")
    lines.append("## Commands")
    lines.append("```bash")
    lines.append("PYTHONPATH=src python experiments/synthetic/run_reciprocal_adversarial_search.py")
    lines.append("PYTHONPATH=src python -m unittest discover -s tests -v")
    lines.append("```")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    results_dir = ROOT / "experiments" / "results"
    docs_dir = ROOT / "docs" / "project-plan"
    results_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    payload = run_adversarial_search()
    metrics_path = results_dir / "reciprocal_adversarial_search_metrics.json"
    note_path = docs_dir / "RECIPROCAL_ADVERSARIAL_FAILURE_SEARCH_2026-04-28.md"
    metrics_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_note(note_path, payload)
    print(f"Wrote {metrics_path}")
    print(f"Wrote {note_path}")
    print(f"Decision: {payload['decision']['decision']}")


if __name__ == "__main__":
    main()
