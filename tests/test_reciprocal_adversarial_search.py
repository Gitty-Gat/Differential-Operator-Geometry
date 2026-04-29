from __future__ import annotations

import unittest

from experiments.synthetic.run_reciprocal_adversarial_search import (
    ADVERSARIAL_CASES,
    PRISM_ADVERSARIAL_CASES,
    SEEDS,
    derive_decision,
    run_adversarial_search,
)


class TestReciprocalAdversarialSearch(unittest.TestCase):
    def test_payload_schema(self) -> None:
        payload = run_adversarial_search()
        self.assertEqual(payload["schema_version"], "reciprocal-adversarial-failure-search-v1")
        self.assertEqual(payload["hard_baseline"], "reciprocal_only")
        self.assertEqual(len(payload["cases"]), len(ADVERSARIAL_CASES))
        self.assertEqual(len(payload["seeds"]), len(SEEDS))
        self.assertEqual(len(payload["prism_scenarios"]), len(PRISM_ADVERSARIAL_CASES))
        self.assertIn(
            payload["decision"]["decision"],
            {"PROMISING_FAILURE_NICHE_FOUND", "FAILURES_FOUND_NO_DOG_RESCUE", "NO_FAILURE_NICHE_FOUND"},
        )

    def test_decision_no_failure_no_niche(self) -> None:
        decision = derive_decision(
            case_summaries=[
                {
                    "case": "mock",
                    "reciprocal_failure": {"any_failure": False},
                    "baseline_comparison": {
                        "rest": {"beats_reciprocal_dog_side": False},
                        "covariance_whitening": {"beats_reciprocal_dog_side": False},
                        "no_transform": {"beats_reciprocal_dog_side": False},
                        "reciprocal_only": {"beats_reciprocal_dog_side": False},
                    },
                }
            ],
            prism_guardrails={
                "rest": {"guardrail_ok_all_scenarios": True},
                "covariance_whitening": {"guardrail_ok_all_scenarios": True},
                "no_transform": {"guardrail_ok_all_scenarios": False},
            },
            reciprocal_contract_summary={"any_contract_failure": False, "failure_scenarios": []},
        )
        self.assertEqual(decision["decision"], "NO_FAILURE_NICHE_FOUND")

    def test_decision_failure_without_guardrail_rescue(self) -> None:
        decision = derive_decision(
            case_summaries=[
                {
                    "case": "mock",
                    "reciprocal_failure": {"any_failure": True},
                    "baseline_comparison": {
                        "rest": {"beats_reciprocal_dog_side": False},
                        "covariance_whitening": {"beats_reciprocal_dog_side": False},
                        "no_transform": {
                            "beats_reciprocal_dog_side": True,
                            "downstream_error_ratio_vs_reciprocal": 0.95,
                            "stability_ratio_vs_reciprocal": 0.90,
                            "runtime_ratio_vs_reciprocal": 0.50,
                        },
                        "reciprocal_only": {"beats_reciprocal_dog_side": False},
                    },
                }
            ],
            prism_guardrails={
                "rest": {"guardrail_ok_all_scenarios": True},
                "covariance_whitening": {"guardrail_ok_all_scenarios": True},
                "no_transform": {"guardrail_ok_all_scenarios": False},
            },
            reciprocal_contract_summary={"any_contract_failure": False, "failure_scenarios": []},
        )
        self.assertEqual(decision["decision"], "FAILURES_FOUND_NO_DOG_RESCUE")


if __name__ == "__main__":
    unittest.main()
