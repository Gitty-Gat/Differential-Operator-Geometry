from __future__ import annotations

import unittest

from experiments.synthetic.run_decision_slice import (
    DecisionSliceConfig,
    RegimeConfig,
    derive_overall_decision,
    run_decision_slice,
)


class TestDecisionSliceHarness(unittest.TestCase):
    def test_small_decision_slice_payload_schema(self) -> None:
        payload = run_decision_slice(
            config=DecisionSliceConfig(steps=48, window_size=12),
            regimes=(RegimeConfig("toy_gap", "toy spectral-gap regime", 2.0, 0.8),),
            seeds=(11, 22),
        )

        self.assertEqual(payload["schema_version"], "decision-slice-v1")
        self.assertEqual(payload["locked_target"]["primary_metrics"], ["stability", "downstream_error", "seed_variance", "runtime"])
        self.assertEqual(len(payload["regimes"]), 1)
        regime = payload["regimes"][0]
        self.assertEqual(set(regime["methods"].keys()), {"rest", "reciprocal_only", "covariance_whitening", "no_transform"})
        self.assertIn(regime["scorecard"]["interpretation"], {"useful", "neutral", "negative"})
        self.assertIn(payload["overall_decision"]["decision"], {"CONTINUE", "REFINE", "PIVOT"})

    def test_pivot_when_reciprocal_matches_or_beats_all(self) -> None:
        summaries = [
            {
                "scorecard": {
                    "interpretation": "negative",
                    "rest_vs_reciprocal_downstream_error_ratio": 1.1,
                    "rest_vs_reciprocal_stability_ratio": 1.2,
                }
            },
            {
                "scorecard": {
                    "interpretation": "negative",
                    "rest_vs_reciprocal_downstream_error_ratio": 1.0,
                    "rest_vs_reciprocal_stability_ratio": 1.0,
                }
            },
        ]
        decision = derive_overall_decision(summaries)
        self.assertEqual(decision["decision"], "PIVOT")


if __name__ == "__main__":
    unittest.main()
