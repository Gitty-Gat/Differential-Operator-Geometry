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

FEATURE_NAMES: Tuple[str, ...] = (
    "posterior_confidence",
    "calibration_score",
    "freshness_age",
    "provenance_present",
    "contradiction_score",
    "decision_trade",
    "decision_artifact_present",
    "approval_token_present",
    "live_write_requested",
    "risk_utilization",
    "heartbeat_age",
    "reconciliation_ok",
    "lineage_integrity",
    "runtime_authorized",
)

METHODS: Tuple[str, ...] = ("rest", "reciprocal_only", "covariance_whitening", "no_transform")


@dataclass(frozen=True)
class PrismMockConfig:
    repeats_per_case: int = 12
    window_size: int = 16
    rank: int = 4
    ridge_scale: float = 0.5
    beta: float = 0.7
    noise_scale: float = 0.025
    seed: int = 717


@dataclass(frozen=True)
class TraceCase:
    family: str
    case: str
    description: str
    vector: Tuple[float, ...]
    contract_pass: int


def base_vector() -> Array:
    return np.array(
        [
            0.78,  # posterior_confidence
            0.82,  # calibration_score
            0.10,  # freshness_age
            1.00,  # provenance_present
            0.00,  # contradiction_score
            0.00,  # decision_trade
            1.00,  # decision_artifact_present
            1.00,  # approval_token_present
            0.00,  # live_write_requested
            0.40,  # risk_utilization
            0.10,  # heartbeat_age
            1.00,  # reconciliation_ok
            1.00,  # lineage_integrity
            1.00,  # runtime_authorized
        ],
        dtype=float,
    )


def make_case(family: str, case: str, description: str, changes: Dict[str, float], contract_pass: int) -> TraceCase:
    v = base_vector()
    name_to_idx = {name: idx for idx, name in enumerate(FEATURE_NAMES)}
    for key, value in changes.items():
        v[name_to_idx[key]] = value
    return TraceCase(family, case, description, tuple(float(x) for x in v), int(contract_pass))


def trace_cases() -> Tuple[TraceCase, ...]:
    return (
        make_case("signal_eligibility", "valid_posterior", "fresh posterior with provenance and calibrated confidence", {}, 1),
        make_case("signal_eligibility", "stale_posterior", "posterior timestamp is stale and must abstain", {"freshness_age": 0.92}, 0),
        make_case("signal_eligibility", "missing_provenance", "posterior lacks provenance hash", {"provenance_present": 0.0, "lineage_integrity": 0.4}, 0),
        make_case("signal_eligibility", "contradictory_evidence", "market evidence is contradictory", {"contradiction_score": 0.88}, 0),
        make_case("signal_eligibility", "low_confidence", "posterior confidence is below signal threshold", {"posterior_confidence": 0.35}, 0),
        make_case("execution_gate", "paper_trade_with_artifact", "paper TRADE decision with decision_artifact_id and approval token", {"decision_trade": 1.0}, 1),
        make_case("execution_gate", "no_trade", "NO_TRADE decision remains non-write", {}, 1),
        make_case("execution_gate", "missing_artifact_id", "TRADE decision lacks decision_artifact_id", {"decision_trade": 1.0, "decision_artifact_present": 0.0, "lineage_integrity": 0.5}, 0),
        make_case("execution_gate", "missing_approval", "TRADE decision lacks explicit approval token", {"decision_trade": 1.0, "approval_token_present": 0.0}, 0),
        make_case("execution_gate", "live_write_requested", "trace attempts live/write action; out of paper-only scope", {"decision_trade": 1.0, "live_write_requested": 1.0}, 0),
        make_case("risk_throttle", "within_limits", "risk utilization is within mocked limits", {}, 1),
        make_case("risk_throttle", "max_notional_breach", "risk utilization exceeds limit", {"risk_utilization": 1.35}, 0),
        make_case("risk_throttle", "concentration_breach", "concentrated exposure represented as high risk utilization", {"risk_utilization": 1.18, "posterior_confidence": 0.9}, 0),
        make_case("risk_throttle", "stale_feed_safe_stop", "stale feed should safe-stop despite otherwise valid signal", {"freshness_age": 0.86, "heartbeat_age": 0.82}, 0),
        make_case("risk_throttle", "drawdown_manual_reset", "drawdown requires manual reset", {"risk_utilization": 1.1, "runtime_authorized": 0.0}, 0),
        make_case("monitoring_invariants", "clean_heartbeat", "fresh heartbeat and reconciliation", {}, 1),
        make_case("monitoring_invariants", "stale_heartbeat", "heartbeat freshness invariant fails", {"heartbeat_age": 0.93}, 0),
        make_case("monitoring_invariants", "contradictory_ticks", "contradictory feed updates", {"contradiction_score": 0.75}, 0),
        make_case("monitoring_invariants", "reconciliation_mismatch", "state reconciliation mismatch", {"reconciliation_ok": 0.0}, 0),
        make_case("monitoring_invariants", "unauthorized_runtime", "runtime label is unauthorized", {"runtime_authorized": 0.0}, 0),
        make_case("artifact_requirements", "complete_manifest", "complete manifest with lineage", {}, 1),
        make_case("artifact_requirements", "missing_manifest_field", "run manifest field is missing", {"lineage_integrity": 0.45}, 0),
        make_case("artifact_requirements", "hash_mismatch", "artifact hash mismatch", {"lineage_integrity": 0.2}, 0),
        make_case("artifact_requirements", "stale_truth_reference", "artifact points at stale current-truth surface", {"lineage_integrity": 0.55, "freshness_age": 0.72}, 0),
        make_case("artifact_requirements", "superseded_packet_reference", "superseded historical packet is treated as current authority", {"lineage_integrity": 0.35, "runtime_authorized": 0.4}, 0),
    )


def generate_trace(config: PrismMockConfig = PrismMockConfig()) -> Tuple[Array, Array, List[Dict[str, object]]]:
    rng = np.random.default_rng(config.seed)
    vectors: List[Array] = []
    labels: List[int] = []
    metadata: List[Dict[str, object]] = []
    for case in trace_cases():
        base = np.array(case.vector, dtype=float)
        for repeat in range(config.repeats_per_case):
            noise = rng.normal(scale=config.noise_scale, size=len(FEATURE_NAMES))
            noisy = np.clip(base + noise, 0.0, 1.5)
            # Preserve hard binary-ish gate fields enough that the mock trace remains interpretable.
            for idx in (3, 5, 6, 7, 8, 11, 13):
                noisy[idx] = 1.0 if noisy[idx] >= 0.5 else 0.0
            vectors.append(noisy)
            labels.append(case.contract_pass)
            metadata.append({"family": case.family, "case": case.case, "description": case.description, "repeat": repeat})
    return np.vstack(vectors), np.asarray(labels, dtype=int), metadata


def covariance_whitening_coordinates(x_t: Array, mean_t: Array, basis_t: Array, eigenvalues_t: Array, ridge_scale: float) -> Array:
    coords = raw_retained_coordinates(x_t, mean_t, basis_t)
    floor = max(EPS, ridge_scale * 1e-6)
    return coords / np.sqrt(np.maximum(eigenvalues_t, floor))


def adjacent_mean_norm(vectors: List[Array]) -> float:
    if len(vectors) < 2:
        return 0.0
    return float(np.mean([np.linalg.norm(vectors[i] - vectors[i - 1]) for i in range(1, len(vectors))]))


def fit_predict_linear_classifier(features: List[Array], labels: List[int]) -> Tuple[Array, Array, Array]:
    x = np.vstack(features)
    y = np.asarray(labels, dtype=float)
    split = max(8, int(0.7 * len(x)))
    x_train, x_test = x[:split], x[split:]
    y_train, y_test = y[:split], y[split:]
    x_train_i = np.column_stack([np.ones(len(x_train)), x_train])
    x_test_i = np.column_stack([np.ones(len(x_test)), x_test])
    ridge = 1e-6 * np.eye(x_train_i.shape[1])
    ridge[0, 0] = 0.0
    coef = np.linalg.solve(x_train_i.T @ x_train_i + ridge, x_train_i.T @ y_train)
    scores = x_test_i @ coef
    pred = (scores >= 0.5).astype(int)
    return pred, y_test.astype(int), scores


def relative_reconstruction_error(original: Array, reconstructed: Array) -> float:
    denom = max(float(np.linalg.norm(original)), EPS)
    return float(np.linalg.norm(original - reconstructed) / denom)


def evaluate_mock_trace(config: PrismMockConfig = PrismMockConfig()) -> Dict[str, object]:
    vectors, labels, metadata = generate_trace(config)
    rest_config = RestConfig(rank=config.rank, ridge_scale=config.ridge_scale, beta=config.beta)
    window = SlidingCovarianceWindow(dimension=len(FEATURE_NAMES), window_size=config.window_size)

    representations: Dict[str, List[Array]] = {method: [] for method in METHODS}
    aligned_labels: List[int] = []
    aligned_meta: List[Dict[str, object]] = []
    transform_times: Dict[str, List[float]] = {method: [] for method in METHODS}
    reconstruction_errors: Dict[str, List[float]] = {method: [] for method in METHODS}

    for idx, x_t in enumerate(vectors):
        window.update(x_t)
        if not window.ready:
            continue
        mean_t = window.mean()
        cov_t = window.covariance()
        basis_t, evals_t = compute_topk_eigendecomposition(cov_t, rank=config.rank)

        start = time.perf_counter()
        step = rest_step(x_t, mean_t, basis_t, evals_t, rest_config, covariance_t=cov_t)
        representations["rest"].append(step.rest_coordinates)
        transform_times["rest"].append((time.perf_counter() - start) * 1000.0)
        rest_recon = mean_t + basis_t @ (step.rest_coordinates / np.maximum(step.composite_weights, EPS))
        reconstruction_errors["rest"].append(relative_reconstruction_error(x_t, rest_recon))

        start = time.perf_counter()
        reciprocal = reciprocal_only_coordinates(x_t, mean_t, basis_t, evals_t, config.ridge_scale, rest_config.reciprocal_clip)
        transform_times["reciprocal_only"].append((time.perf_counter() - start) * 1000.0)
        representations["reciprocal_only"].append(reciprocal)
        inv_weights = np.clip(
            np.power(evals_t + config.ridge_scale, -0.5),
            rest_config.reciprocal_clip[0],
            rest_config.reciprocal_clip[1],
        )
        recip_recon = mean_t + basis_t @ (reciprocal / np.maximum(inv_weights, EPS))
        reconstruction_errors["reciprocal_only"].append(relative_reconstruction_error(x_t, recip_recon))

        start = time.perf_counter()
        whitening = covariance_whitening_coordinates(x_t, mean_t, basis_t, evals_t, config.ridge_scale)
        transform_times["covariance_whitening"].append((time.perf_counter() - start) * 1000.0)
        representations["covariance_whitening"].append(whitening)
        whitening_recon = mean_t + basis_t @ (whitening * np.sqrt(np.maximum(evals_t, config.ridge_scale * 1e-6)))
        reconstruction_errors["covariance_whitening"].append(relative_reconstruction_error(x_t, whitening_recon))

        start = time.perf_counter()
        no_transform = x_t.copy()
        transform_times["no_transform"].append((time.perf_counter() - start) * 1000.0)
        representations["no_transform"].append(no_transform)
        reconstruction_errors["no_transform"].append(0.0)

        aligned_labels.append(int(labels[idx]))
        aligned_meta.append(metadata[idx])

    method_metrics: Dict[str, Dict[str, float]] = {}
    for method, feats in representations.items():
        pred, y_test, _scores = fit_predict_linear_classifier(feats, aligned_labels)
        error = float(np.mean(pred != y_test))
        false_pass = float(np.mean((pred == 1) & (y_test == 0))) if len(y_test) else 0.0
        false_block = float(np.mean((pred == 0) & (y_test == 1))) if len(y_test) else 0.0
        method_metrics[method] = {
            "contract_classification_error": error,
            "false_pass_rate": false_pass,
            "false_block_rate": false_block,
            "stability": adjacent_mean_norm(feats),
            "runtime_ms_mean": float(np.mean(transform_times[method])) if transform_times[method] else 0.0,
            "auditability_reconstruction_error": float(np.mean(reconstruction_errors[method])) if reconstruction_errors[method] else 0.0,
        }

    rest = method_metrics["rest"]
    reciprocal = method_metrics["reciprocal_only"]
    no_transform = method_metrics["no_transform"]
    reciprocal_enough = (
        reciprocal["contract_classification_error"] <= rest["contract_classification_error"] + 0.01
        and reciprocal["false_pass_rate"] <= rest["false_pass_rate"] + 0.01
        and reciprocal["runtime_ms_mean"] <= rest["runtime_ms_mean"]
    )
    transforms_obscure = any(
        method_metrics[m]["auditability_reconstruction_error"] > 0.20 for m in ("rest", "reciprocal_only", "covariance_whitening")
    ) and no_transform["auditability_reconstruction_error"] == 0.0

    if reciprocal_enough or transforms_obscure:
        decision = "STOP_OR_REFINE"
        if reciprocal_enough and transforms_obscure:
            rationale = "Paper/mock trace evidence does not justify promoting current REST: reciprocal-only remains sufficient and spectral transforms lose too much contract-field auditability relative to no-transform."
        elif reciprocal_enough:
            rationale = "Paper/mock trace evidence does not justify promoting current REST: reciprocal-only matches REST on contract classification and false-pass risk while running faster and producing a more stable representation."
        else:
            rationale = "Paper/mock trace evidence does not justify promoting current REST: spectral transforms lose too much contract-field auditability relative to no-transform."
    else:
        decision = "CONTINUE_BOUNDED_SPIKE"
        rationale = "A DOG transform shows a contract-gate benefit without worse false-pass risk or auditability loss; continue only as paper/mock work."

    return {
        "schema_version": "dog-prism-contract-mock-v1",
        "mode": "paper_mock_only",
        "authority_boundary": "No live credentials, no live/write calls, no widened PRISM authority.",
        "prism_gate_artifacts_referenced": [
            "docs/project-plan/THEOREM_TO_CONTRACT_GATE.md",
            "docs/project-plan/STATUS_BOARD.md",
            "docs/project-plan/VERIFICATION_MATRIX.md",
            "docs/project-plan/DOG_PRISM_ARCHITECTURE_SPIKE_PLAN_2026-04-28.md",
        ],
        "dog_context_artifacts_referenced": [
            "docs/project-plan/CHAIRMAN_DECISION_SLICE_EVALUATION_NOTE_2026-04-28.md",
            "experiments/results/decision_slice_metrics.json",
        ],
        "feature_names": list(FEATURE_NAMES),
        "config": asdict(config),
        "trace_case_count": len(trace_cases()),
        "samples_evaluated": len(aligned_labels),
        "methods": method_metrics,
        "scorecard": {
            "reciprocal_only_remains_enough": bool(reciprocal_enough),
            "transforms_obscure_contract_fields": bool(transforms_obscure),
            "decision": decision,
            "rationale": rationale,
        },
    }


def write_note(path: Path, payload: Dict[str, object]) -> None:
    lines: List[str] = []
    lines.append("# DOG×PRISM Contract-Gate Mock Evaluation — 2026-04-28")
    lines.append("")
    lines.append("## Status")
    lines.append("Paper/mock-only DOG-owned follow-on artifact for the approved DOG×PRISM bounded spike.")
    lines.append("")
    lines.append("## Authority boundary")
    lines.append("No live credentials, no production reads/writes, no order placement, no new PRISM write path, and no claim that current REST is validated for PRISM live use.")
    lines.append("")
    lines.append("## PRISM artifacts coordinated")
    for item in payload["prism_gate_artifacts_referenced"]:
        lines.append(f"- PRISM `{item}`")
    lines.append("")
    lines.append("## DOG artifacts coordinated")
    for item in payload["dog_context_artifacts_referenced"]:
        lines.append(f"- DOG `{item}`")
    lines.append("")
    lines.append("## Protocol")
    lines.append("Simulated PRISM contract-gate traces are encoded as numeric paper/mock vectors covering signal eligibility, execution gating, risk throttles, monitoring invariants, and artifact requirements. DOG compares current REST against reciprocal-only, covariance-whitening, and no-transform.")
    lines.append("")
    lines.append("## Metrics")
    lines.append("- contract classification error")
    lines.append("- false-pass rate, i.e. invalid contract state classified as pass")
    lines.append("- false-block rate")
    lines.append("- representation stability")
    lines.append("- runtime")
    lines.append("- auditability reconstruction error")
    lines.append("")
    lines.append("## Results")
    lines.append("| Method | Contract error | False pass | False block | Stability | Runtime ms | Auditability loss |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for method, metrics in payload["methods"].items():
        lines.append(
            f"| {method} | {metrics['contract_classification_error']:.6f} | {metrics['false_pass_rate']:.6f} | {metrics['false_block_rate']:.6f} | {metrics['stability']:.6f} | {metrics['runtime_ms_mean']:.6f} | {metrics['auditability_reconstruction_error']:.6f} |"
        )
    lines.append("")
    lines.append("## Decision")
    lines.append(f"**{payload['scorecard']['decision']}**")
    lines.append("")
    lines.append(payload["scorecard"]["rationale"])
    lines.append("")
    lines.append("## Stop conditions applied")
    lines.append(f"- reciprocal-only remains enough: `{str(payload['scorecard']['reciprocal_only_remains_enough']).lower()}`")
    lines.append(f"- transforms obscure contract fields: `{str(payload['scorecard']['transforms_obscure_contract_fields']).lower()}`")
    lines.append("- live/write access required: `false`")
    lines.append("")
    lines.append("## Verification command")
    lines.append("```bash")
    lines.append("PYTHONPATH=src python experiments/synthetic/run_prism_contract_mock.py")
    lines.append("```")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    results_dir = ROOT / "experiments" / "results"
    docs_dir = ROOT / "docs" / "project-plan"
    results_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    payload = evaluate_mock_trace()
    metrics_path = results_dir / "prism_contract_mock_metrics.json"
    note_path = docs_dir / "DOG_PRISM_CONTRACT_MOCK_EVALUATION_2026-04-28.md"
    metrics_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_note(note_path, payload)
    print(f"Wrote {metrics_path}")
    print(f"Wrote {note_path}")
    print(f"Decision: {payload['scorecard']['decision']}")


if __name__ == "__main__":
    main()
