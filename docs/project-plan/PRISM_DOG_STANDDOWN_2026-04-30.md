# PRISM↔DOG Stand-Down — 2026-04-30

## Status
Chairman directive: PRISM↔DOG collaboration is stood down for now. DOG should preserve the paper/mock artifacts already produced, but should stop spending cycles on PRISM integration, PRISM theorem-to-contract service work, or PRISM-specific guardrail expansion unless explicitly reauthorized.

## What remains preserved
The following artifacts remain useful as historical evidence and claim-control material:
- `docs/project-plan/DOG_PRISM_ARCHITECTURE_SPIKE_PLAN_2026-04-28.md`
- `docs/project-plan/DOG_PRISM_CONTRACT_MOCK_EVALUATION_2026-04-28.md`
- `experiments/synthetic/run_prism_contract_mock.py`
- `experiments/results/prism_contract_mock_metrics.json`

They showed that current REST did not earn a PRISM-facing claim: reciprocal-only matched REST on paper/mock contract classification and false-pass risk while running faster and producing a more stable representation.

## What changes now
Effective immediately:
- PRISM is no longer an active DOG customer, integration target, or required next-slice guardrail.
- DOG should not modify PRISM, inspect PRISM for follow-up work, or run PRISM-specific evaluation as a default step.
- DOG should not claim REST helps PRISM.
- DOG may cite the archived PRISM mock only as historical evidence that current REST did not earn a PRISM-facing claim.
- Future DOG variants should be judged first on DOG-local evidence: reciprocal-only baseline, downstream error, stability, runtime, reconstructability/auditability, and claim control.

## Replacement active direction
DOG's active path is now:
1. preserve the PIVOT / robustness / adversarial evidence;
2. treat reciprocal-only as the hard baseline and likely narrowed contribution;
3. stop trying to rescue current REST unless a genuinely new, pre-registered variant is proposed;
4. produce a scope-demotion / reciprocal-only characterization note before any further architecture work;
5. keep theorem and method prose subordinate to benchmark evidence.

## Verification posture
Routine DOG verification should prefer DOG-local commands:
```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python experiments/synthetic/run_decision_slice.py
PYTHONPATH=src python experiments/synthetic/run_reciprocal_robustness_sweep.py
PYTHONPATH=src python experiments/synthetic/run_reciprocal_adversarial_search.py
```

`experiments/synthetic/run_prism_contract_mock.py` remains runnable for archival reproducibility, but it is no longer part of the default forward plan unless PRISM↔DOG collaboration is explicitly reauthorized.
