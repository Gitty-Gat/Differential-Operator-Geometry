from __future__ import annotations

import unittest

from experiments.synthetic.run_prism_contract_mock import (
    FEATURE_NAMES,
    METHODS,
    PrismMockConfig,
    evaluate_mock_trace,
    generate_trace,
    trace_cases,
)


class TestPrismContractMockHarness(unittest.TestCase):
    def test_trace_cases_cover_five_contract_families(self) -> None:
        families = {case.family for case in trace_cases()}
        self.assertEqual(
            families,
            {
                "signal_eligibility",
                "execution_gate",
                "risk_throttle",
                "monitoring_invariants",
                "artifact_requirements",
            },
        )

    def test_generate_trace_shape_and_labels(self) -> None:
        config = PrismMockConfig(repeats_per_case=2, window_size=8)
        vectors, labels, metadata = generate_trace(config)
        self.assertEqual(vectors.shape[1], len(FEATURE_NAMES))
        self.assertEqual(len(labels), len(metadata))
        self.assertEqual(len(labels), len(trace_cases()) * 2)
        self.assertGreater(int(labels.sum()), 0)
        self.assertGreater(len(labels) - int(labels.sum()), 0)

    def test_evaluation_payload_schema(self) -> None:
        payload = evaluate_mock_trace(PrismMockConfig(repeats_per_case=3, window_size=8, rank=3))
        self.assertEqual(payload["schema_version"], "dog-prism-contract-mock-v1")
        self.assertEqual(payload["mode"], "paper_mock_only")
        self.assertEqual(set(payload["methods"].keys()), set(METHODS))
        self.assertIn(payload["scorecard"]["decision"], {"STOP_OR_REFINE", "CONTINUE_BOUNDED_SPIKE"})
        for metrics in payload["methods"].values():
            self.assertIn("contract_classification_error", metrics)
            self.assertIn("false_pass_rate", metrics)
            self.assertIn("auditability_reconstruction_error", metrics)


if __name__ == "__main__":
    unittest.main()
