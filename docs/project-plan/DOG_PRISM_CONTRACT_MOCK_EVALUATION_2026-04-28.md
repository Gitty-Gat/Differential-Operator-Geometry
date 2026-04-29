# DOG×PRISM Contract-Gate Mock Evaluation — 2026-04-28

## Status
Paper/mock-only DOG-owned follow-on artifact for the approved DOG×PRISM bounded spike.

## Authority boundary
No live credentials, no production reads/writes, no order placement, no new PRISM write path, and no claim that current REST is validated for PRISM live use.

## PRISM artifacts coordinated
- PRISM `docs/project-plan/THEOREM_TO_CONTRACT_GATE.md`
- PRISM `docs/project-plan/STATUS_BOARD.md`
- PRISM `docs/project-plan/VERIFICATION_MATRIX.md`
- PRISM `docs/project-plan/DOG_PRISM_ARCHITECTURE_SPIKE_PLAN_2026-04-28.md`

## DOG artifacts coordinated
- DOG `docs/project-plan/CHAIRMAN_DECISION_SLICE_EVALUATION_NOTE_2026-04-28.md`
- DOG `experiments/results/decision_slice_metrics.json`

## Protocol
Simulated PRISM contract-gate traces are encoded as numeric paper/mock vectors covering signal eligibility, execution gating, risk throttles, monitoring invariants, and artifact requirements. DOG compares current REST against reciprocal-only, covariance-whitening, and no-transform.

## Metrics
- contract classification error
- false-pass rate, i.e. invalid contract state classified as pass
- false-block rate
- representation stability
- runtime
- auditability reconstruction error

## Results
| Method | Contract error | False pass | False block | Stability | Runtime ms | Auditability loss |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rest | 0.139535 | 0.000000 | 0.139535 | 0.430556 | 0.027092 | 0.008306 |
| reciprocal_only | 0.139535 | 0.000000 | 0.139535 | 0.367995 | 0.008234 | 0.008306 |
| covariance_whitening | 0.139535 | 0.000000 | 0.139535 | 2.556958 | 0.004587 | 0.008306 |
| no_transform | 0.790698 | 0.790698 | 0.000000 | 0.168270 | 0.000725 | 0.000000 |

## Decision
**STOP_OR_REFINE**

Paper/mock trace evidence does not justify promoting current REST: reciprocal-only matches REST on contract classification and false-pass risk while running faster and producing a more stable representation.

## Stop conditions applied
- reciprocal-only remains enough: `true`
- transforms obscure contract fields: `false`
- live/write access required: `false`

## Verification command
```bash
PYTHONPATH=src python experiments/synthetic/run_prism_contract_mock.py
```
