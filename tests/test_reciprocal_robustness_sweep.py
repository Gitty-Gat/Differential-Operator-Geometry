from __future__ import annotations

import unittest

from experiments.synthetic.run_reciprocal_robustness_sweep import (
    DOG_REGIMES,
    DOG_SCENARIOS,
    PRISM_SCENARIOS,
    derive_decision,
    evaluate_prism_guardrails,
    run_robustness_sweep,
)


class TestReciprocalRobustnessSweep(unittest.TestCase):
    def test_sweep_payload_schema(self) -> None:
        payload = run_robustness_sweep()
        self.assertEqual(payload["schema_version"], "reciprocal-robustness-sweep-v1")
        self.assertEqual(payload["hard_baseline"], "reciprocal_only")
        self.assertEqual(len(payload["dog_summaries"]), len(DOG_SCENARIOS) * len(DOG_REGIMES))
        self.assertEqual(len(payload["prism_scenarios"]), len(PRISM_SCENARIOS))
        self.assertIn(
            payload["decision"]["decision"],
            {"RECIPROCAL_BASELINE_REMAINS_ENOUGH", "REFINE_AROUND_FAILURE_REGIME"},
        )

    def test_prism_guardrails_include_non_reciprocal_methods(self) -> None:
        _scenarios, guardrails = evaluate_prism_guardrails()
        self.assertIn("rest", guardrails)
        self.assertIn("covariance_whitening", guardrails)
        self.assertIn("no_transform", guardrails)
        for metrics in guardrails.values():
            self.assertIn("guardrail_ok_all_scenarios", metrics)
            self.assertIn("max_false_pass_delta_vs_reciprocal", metrics)
            self.assertIn("max_auditability_delta_vs_reciprocal", metrics)

    def test_decision_defaults_to_reciprocal_enough_without_qualified_wins(self) -> None:
        decision = derive_decision(
            dog_summaries=[
                {
                    "scenario": "mock",
                    "name": "regime",
                    "baseline_comparison": {
                        "rest": {
                            "downstream_error_ratio_vs_reciprocal": 1.0,
                            "stability_ratio_vs_reciprocal": 1.0,
                            "runtime_ratio_vs_reciprocal": 1.0,
                            "material_downstream_win": False,
                            "dog_win_vs_reciprocal": False,
                        },
                        "covariance_whitening": {
                            "downstream_error_ratio_vs_reciprocal": 0.99,
                            "stability_ratio_vs_reciprocal": 1.0,
                            "runtime_ratio_vs_reciprocal": 1.0,
                            "material_downstream_win": False,
                            "dog_win_vs_reciprocal": False,
                        },
                        "no_transform": {
                            "downstream_error_ratio_vs_reciprocal": 0.97,
                            "stability_ratio_vs_reciprocal": 1.0,
                            "runtime_ratio_vs_reciprocal": 1.0,
                            "material_downstream_win": True,
                            "dog_win_vs_reciprocal": True,
                        },
                        "reciprocal_only": {},
                    },
                }
            ],
            prism_method_guardrails={
                "rest": {"guardrail_ok_all_scenarios": True},
                "covariance_whitening": {"guardrail_ok_all_scenarios": True},
                "no_transform": {"guardrail_ok_all_scenarios": False},
            },
        )
        self.assertEqual(decision["decision"], "RECIPROCAL_BASELINE_REMAINS_ENOUGH")


if __name__ == "__main__":
    unittest.main()
