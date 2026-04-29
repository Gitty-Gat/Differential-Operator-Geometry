from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from run_decision_slice import (  # noqa: E402
    DecisionSliceConfig,
    METHODS as DOG_METHODS,
    RegimeConfig,
    aggregate_regime,
    evaluate_regime_seed,
    format_float,
)
from run_prism_contract_mock import METHODS as PRISM_METHODS, PrismMockConfig, evaluate_mock_trace  # noqa: E402

DOG_SEEDS: Tuple[int, ...] = (101, 202, 303, 404, 505, 606, 707)

DOG_REGIMES: Tuple[RegimeConfig, ...] = (
    RegimeConfig("clean_gap", "clear dominant spectral direction", 3.0, 0.45),
    RegimeConfig("medium_gap", "present but less dominant spectral gap", 2.1, 0.9),
    RegimeConfig("messy_gap", "weak / messy top-two separation", 1.45, 1.15),
    RegimeConfig("near_isotropic", "almost no retained spectral separation", 1.12, 1.05),
    RegimeConfig("extreme_gap", "very strong dominant spectral direction", 4.2, 0.18),
)


@dataclass(frozen=True)
class DogSweepScenario:
    name: str
    description: str
    config: DecisionSliceConfig


DOG_SCENARIOS: Tuple[DogSweepScenario, ...] = (
    DogSweepScenario("locked_default", "locked moderate-drift decision-slice parameters", DecisionSliceConfig()),
    DogSweepScenario("fast_rotation", "faster covariance eigenspace rotation", DecisionSliceConfig(rotation_speed=0.085)),
    DogSweepScenario("high_observation_noise", "higher observation noise around the latent manifold", DecisionSliceConfig(observation_noise=0.18)),
    DogSweepScenario("low_persistence", "weaker temporal persistence in the latent state", DecisionSliceConfig(latent_persistence=0.45)),
    DogSweepScenario("short_window", "shorter covariance window under the same drift", DecisionSliceConfig(window_size=14)),
    DogSweepScenario("long_window", "longer covariance window under the same drift", DecisionSliceConfig(window_size=52)),
    DogSweepScenario("higher_rank_noise", "rank-three retained subspace in a noisier eight-dimensional stream", DecisionSliceConfig(dimension=8, rank=3, window_size=32, observation_noise=0.12)),
)


@dataclass(frozen=True)
class PrismSweepScenario:
    name: str
    description: str
    config: PrismMockConfig


PRISM_SCENARIOS: Tuple[PrismSweepScenario, ...] = (
    PrismSweepScenario("default_mock", "current DOG×PRISM paper/mock contract trace", PrismMockConfig()),
    PrismSweepScenario("noisier_mock", "higher feature noise in paper/mock contract trace", PrismMockConfig(noise_scale=0.06, seed=818)),
    PrismSweepScenario("short_window_mock", "shorter PRISM trace covariance window", PrismMockConfig(window_size=8, seed=919)),
    PrismSweepScenario("low_rank_mock", "lower retained rank for contract trace", PrismMockConfig(rank=2, seed=1020)),
)

MATERIAL_ERROR_WIN = 0.98
STABILITY_GUARDRAIL = 1.10
RUNTIME_GUARDRAIL = 3.00
AUDITABILITY_TOLERANCE = 1e-9
FALSE_PASS_TOLERANCE = 1e-9


def ratio(numerator: float, denominator: float) -> float:
    denom = denominator if abs(denominator) > 1e-12 else 1e-12
    return float(numerator / denom)


def evaluate_dog_sweep() -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    summaries: List[Dict[str, object]] = []
    raw_runs: List[Dict[str, object]] = []
    for scenario in DOG_SCENARIOS:
        for regime in DOG_REGIMES:
            seed_results = [evaluate_regime_seed(regime, config=scenario.config, seed=seed) for seed in DOG_SEEDS]
            raw_runs.extend({"scenario": scenario.name, **result} for result in seed_results)
            aggregate = aggregate_regime(regime, seed_results)
            aggregate["scenario"] = scenario.name
            aggregate["scenario_description"] = scenario.description
            aggregate["config"] = asdict(scenario.config)
            reciprocal = aggregate["methods"]["reciprocal_only"]
            comparisons: Dict[str, Dict[str, object]] = {}
            for method in DOG_METHODS:
                metrics = aggregate["methods"][method]
                error_ratio = ratio(metrics["downstream_error_mean"], reciprocal["downstream_error_mean"])
                stability_ratio = ratio(metrics["stability_mean"], reciprocal["stability_mean"])
                runtime_ratio = ratio(metrics["runtime_ms_mean"], reciprocal["runtime_ms_mean"])
                comparisons[method] = {
                    "downstream_error_ratio_vs_reciprocal": error_ratio,
                    "stability_ratio_vs_reciprocal": stability_ratio,
                    "runtime_ratio_vs_reciprocal": runtime_ratio,
                    "material_downstream_win": bool(error_ratio <= MATERIAL_ERROR_WIN),
                    "stability_guardrail_ok": bool(stability_ratio <= STABILITY_GUARDRAIL),
                    "runtime_guardrail_ok": bool(runtime_ratio <= RUNTIME_GUARDRAIL),
                    "dog_win_vs_reciprocal": bool(
                        method != "reciprocal_only"
                        and error_ratio <= MATERIAL_ERROR_WIN
                        and stability_ratio <= STABILITY_GUARDRAIL
                        and runtime_ratio <= RUNTIME_GUARDRAIL
                    ),
                }
            aggregate["baseline_comparison"] = comparisons
            summaries.append(aggregate)
    return summaries, raw_runs


def evaluate_prism_guardrails() -> Tuple[List[Dict[str, object]], Dict[str, Dict[str, object]]]:
    scenario_results: List[Dict[str, object]] = []
    per_method: Dict[str, Dict[str, object]] = {
        method: {
            "max_contract_error_delta_vs_reciprocal": -float("inf"),
            "max_false_pass_delta_vs_reciprocal": -float("inf"),
            "max_auditability_delta_vs_reciprocal": -float("inf"),
            "max_stability_ratio_vs_reciprocal": -float("inf"),
            "guardrail_ok_all_scenarios": True,
        }
        for method in PRISM_METHODS
        if method != "reciprocal_only"
    }

    for scenario in PRISM_SCENARIOS:
        payload = evaluate_mock_trace(scenario.config)
        methods = payload["methods"]
        reciprocal = methods["reciprocal_only"]
        comparisons: Dict[str, Dict[str, object]] = {}
        for method, metrics in methods.items():
            contract_error_delta = metrics["contract_classification_error"] - reciprocal["contract_classification_error"]
            false_pass_delta = metrics["false_pass_rate"] - reciprocal["false_pass_rate"]
            auditability_delta = metrics["auditability_reconstruction_error"] - reciprocal["auditability_reconstruction_error"]
            stability_ratio = ratio(metrics["stability"], reciprocal["stability"])
            guardrail_ok = bool(
                false_pass_delta <= FALSE_PASS_TOLERANCE
                and auditability_delta <= AUDITABILITY_TOLERANCE
                and not payload["scorecard"]["transforms_obscure_contract_fields"]
            )
            comparisons[method] = {
                "contract_error_delta_vs_reciprocal": float(contract_error_delta),
                "false_pass_delta_vs_reciprocal": float(false_pass_delta),
                "auditability_delta_vs_reciprocal": float(auditability_delta),
                "stability_ratio_vs_reciprocal": float(stability_ratio),
                "guardrail_ok": guardrail_ok,
            }
            if method != "reciprocal_only":
                m = per_method[method]
                m["max_contract_error_delta_vs_reciprocal"] = max(m["max_contract_error_delta_vs_reciprocal"], float(contract_error_delta))
                m["max_false_pass_delta_vs_reciprocal"] = max(m["max_false_pass_delta_vs_reciprocal"], float(false_pass_delta))
                m["max_auditability_delta_vs_reciprocal"] = max(m["max_auditability_delta_vs_reciprocal"], float(auditability_delta))
                m["max_stability_ratio_vs_reciprocal"] = max(m["max_stability_ratio_vs_reciprocal"], float(stability_ratio))
                m["guardrail_ok_all_scenarios"] = bool(m["guardrail_ok_all_scenarios"] and guardrail_ok)
        scenario_results.append(
            {
                "scenario": scenario.name,
                "description": scenario.description,
                "config": asdict(scenario.config),
                "decision": payload["scorecard"]["decision"],
                "reciprocal_only_remains_enough": payload["scorecard"]["reciprocal_only_remains_enough"],
                "transforms_obscure_contract_fields": payload["scorecard"]["transforms_obscure_contract_fields"],
                "methods": methods,
                "baseline_comparison": comparisons,
            }
        )
    return scenario_results, per_method


def derive_decision(
    dog_summaries: List[Dict[str, object]],
    prism_method_guardrails: Dict[str, Dict[str, object]],
) -> Dict[str, object]:
    dog_wins_by_method: Dict[str, List[Dict[str, object]]] = {m: [] for m in DOG_METHODS if m != "reciprocal_only"}
    downstream_only_by_method: Dict[str, List[Dict[str, object]]] = {m: [] for m in DOG_METHODS if m != "reciprocal_only"}
    for summary in dog_summaries:
        for method, comparison in summary["baseline_comparison"].items():
            if method == "reciprocal_only":
                continue
            record = {
                "scenario": summary["scenario"],
                "regime": summary["name"],
                "downstream_error_ratio_vs_reciprocal": comparison["downstream_error_ratio_vs_reciprocal"],
                "stability_ratio_vs_reciprocal": comparison["stability_ratio_vs_reciprocal"],
                "runtime_ratio_vs_reciprocal": comparison["runtime_ratio_vs_reciprocal"],
            }
            if comparison["dog_win_vs_reciprocal"]:
                dog_wins_by_method[method].append(record)
            elif comparison["material_downstream_win"]:
                downstream_only_by_method[method].append(record)

    qualified_wins: Dict[str, List[Dict[str, object]]] = {}
    for method, wins in dog_wins_by_method.items():
        if wins and prism_method_guardrails.get(method, {}).get("guardrail_ok_all_scenarios", False):
            qualified_wins[method] = wins

    if qualified_wins:
        decision = "REFINE_AROUND_FAILURE_REGIME"
        rationale = "At least one non-reciprocal method produced a material DOG win while preserving PRISM mock false-pass and auditability guardrails; treat only those regimes as candidate failure cases for reciprocal-only."
    else:
        decision = "RECIPROCAL_BASELINE_REMAINS_ENOUGH"
        rationale = "No method beat reciprocal-only on the material DOG win rule while also satisfying PRISM mock false-pass and auditability guardrails across the sweep."

    return {
        "decision": decision,
        "rationale": rationale,
        "qualified_wins": qualified_wins,
        "dog_wins_by_method": dog_wins_by_method,
        "downstream_only_wins_by_method": downstream_only_by_method,
    }


def run_robustness_sweep() -> Dict[str, object]:
    dog_summaries, dog_raw_runs = evaluate_dog_sweep()
    prism_summaries, prism_guardrails = evaluate_prism_guardrails()
    decision = derive_decision(dog_summaries, prism_guardrails)
    return {
        "schema_version": "reciprocal-robustness-sweep-v1",
        "mode": "paper_mock_and_synthetic_only",
        "hard_baseline": "reciprocal_only",
        "claim_boundary": "No claim that REST helps PRISM; identify only benchmarked failure regimes or stop/refine.",
        "materiality_rule": {
            "downstream_error_ratio_vs_reciprocal_max": MATERIAL_ERROR_WIN,
            "stability_ratio_vs_reciprocal_max": STABILITY_GUARDRAIL,
            "runtime_ratio_vs_reciprocal_max": RUNTIME_GUARDRAIL,
            "false_pass_delta_vs_reciprocal_max": FALSE_PASS_TOLERANCE,
            "auditability_delta_vs_reciprocal_max": AUDITABILITY_TOLERANCE,
        },
        "dog_scenarios": [
            {"name": s.name, "description": s.description, "config": asdict(s.config)} for s in DOG_SCENARIOS
        ],
        "dog_regimes": [asdict(r) for r in DOG_REGIMES],
        "dog_seeds": list(DOG_SEEDS),
        "dog_summaries": dog_summaries,
        "dog_raw_runs": dog_raw_runs,
        "prism_scenarios": prism_summaries,
        "prism_method_guardrails": prism_guardrails,
        "decision": decision,
    }


def write_note(path: Path, payload: Dict[str, object]) -> None:
    lines: List[str] = []
    lines.append("# Reciprocal-Only Robustness / Failure-Regime Sweep — 2026-04-28")
    lines.append("")
    lines.append("## Status")
    lines.append("Executed post-PIVOT robustness slice. Reciprocal-only is the hard baseline.")
    lines.append("")
    lines.append("## Claim boundary")
    lines.append("No theorem prose in place of benchmark evidence. No claim that REST helps PRISM. This is synthetic DOG evidence plus paper/mock PRISM guardrail evidence only.")
    lines.append("")
    lines.append("## Protocol")
    lines.append("The sweep reuses the locked DOG decision-slice evaluator across additional seed/regime/scenario combinations, then checks PRISM paper/mock false-pass and auditability guardrails across multiple mock configurations.")
    lines.append("")
    lines.append("A non-reciprocal method counts as a qualified reciprocal-only failure case only when all of the following hold:")
    lines.append(f"- downstream error ratio vs reciprocal-only <= `{MATERIAL_ERROR_WIN}`;")
    lines.append(f"- stability ratio vs reciprocal-only <= `{STABILITY_GUARDRAIL}`;")
    lines.append(f"- runtime ratio vs reciprocal-only <= `{RUNTIME_GUARDRAIL}`;")
    lines.append("- PRISM mock false-pass risk is not worse than reciprocal-only;")
    lines.append("- PRISM mock auditability loss is not worse than reciprocal-only;")
    lines.append("- PRISM mock contract fields are not obscured.")
    lines.append("")
    lines.append("## DOG sweep coverage")
    lines.append(f"- Scenarios: `{len(payload['dog_scenarios'])}`")
    lines.append(f"- Regimes per scenario: `{len(payload['dog_regimes'])}`")
    lines.append(f"- Seeds per scenario/regime: `{len(payload['dog_seeds'])}`")
    lines.append(f"- Scenario/regime summaries: `{len(payload['dog_summaries'])}`")
    lines.append("")
    lines.append("## PRISM guardrail coverage")
    lines.append(f"- Paper/mock scenarios: `{len(payload['prism_scenarios'])}`")
    lines.append("- Guardrails: false-pass delta, auditability delta, contract-obscurity flag")
    lines.append("")
    lines.append("## Decision")
    lines.append(f"**{payload['decision']['decision']}**")
    lines.append("")
    lines.append(payload["decision"]["rationale"])
    lines.append("")
    lines.append("## Qualified reciprocal-only failure cases")
    if payload["decision"]["qualified_wins"]:
        for method, wins in payload["decision"]["qualified_wins"].items():
            lines.append(f"### {method}")
            for win in wins:
                lines.append(
                    f"- `{win['scenario']}` / `{win['regime']}`: error ratio `{format_float(win['downstream_error_ratio_vs_reciprocal'])}`, stability ratio `{format_float(win['stability_ratio_vs_reciprocal'])}`, runtime ratio `{format_float(win['runtime_ratio_vs_reciprocal'])}`"
                )
    else:
        lines.append("None under the registered materiality + PRISM-guardrail rule.")
    lines.append("")
    lines.append("## DOG downstream-only signals that failed at least one guardrail")
    any_downstream_only = False
    for method, wins in payload["decision"]["downstream_only_wins_by_method"].items():
        if not wins:
            continue
        any_downstream_only = True
        lines.append(f"### {method}")
        for win in wins[:12]:
            lines.append(
                f"- `{win['scenario']}` / `{win['regime']}`: error ratio `{format_float(win['downstream_error_ratio_vs_reciprocal'])}`, stability ratio `{format_float(win['stability_ratio_vs_reciprocal'])}`, runtime ratio `{format_float(win['runtime_ratio_vs_reciprocal'])}`"
            )
        if len(wins) > 12:
            lines.append(f"- ... `{len(wins) - 12}` more in metrics JSON")
    if not any_downstream_only:
        lines.append("None.")
    lines.append("")
    lines.append("## PRISM method guardrails")
    lines.append("| Method | Guardrail OK all scenarios | Max contract-error delta | Max false-pass delta | Max auditability delta | Max stability ratio |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    for method, metrics in payload["prism_method_guardrails"].items():
        lines.append(
            f"| {method} | {str(metrics['guardrail_ok_all_scenarios']).lower()} | {format_float(metrics['max_contract_error_delta_vs_reciprocal'])} | {format_float(metrics['max_false_pass_delta_vs_reciprocal'])} | {format_float(metrics['max_auditability_delta_vs_reciprocal'])} | {format_float(metrics['max_stability_ratio_vs_reciprocal'])} |"
        )
    lines.append("")
    lines.append("## Interpretation")
    if payload["decision"]["decision"] == "RECIPROCAL_BASELINE_REMAINS_ENOUGH":
        lines.append("Reciprocal-only remains enough for this robustness slice. Some methods may show downstream-only wins, but no method earns a post-PIVOT continuation claim unless it also clears stability, runtime, false-pass, and auditability guardrails.")
    else:
        lines.append("The qualified cases are candidate reciprocal-only failure regimes only. They do not validate current REST broadly and do not imply PRISM live usefulness.")
    lines.append("")
    lines.append("## Commands")
    lines.append("```bash")
    lines.append("PYTHONPATH=src python experiments/synthetic/run_reciprocal_robustness_sweep.py")
    lines.append("PYTHONPATH=src python -m unittest discover -s tests -v")
    lines.append("```")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    results_dir = ROOT / "experiments" / "results"
    docs_dir = ROOT / "docs" / "project-plan"
    results_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    payload = run_robustness_sweep()
    metrics_path = results_dir / "reciprocal_robustness_sweep_metrics.json"
    note_path = docs_dir / "RECIPROCAL_ROBUSTNESS_SWEEP_2026-04-28.md"
    metrics_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_note(note_path, payload)
    print(f"Wrote {metrics_path}")
    print(f"Wrote {note_path}")
    print(f"Decision: {payload['decision']['decision']}")


if __name__ == "__main__":
    main()
