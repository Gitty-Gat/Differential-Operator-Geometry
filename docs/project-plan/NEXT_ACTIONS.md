# NEXT_ACTIONS

_Last updated: 2026-04-28_

This file is the short operational queue for the repo. It exists to turn the current framing into the next few resumable slices without re-reading the entire project history.

## Active objective
Respond to the combined DOG and DOG×PRISM paper/mock results:

> DOG PIVOT — reciprocal-only matched or beat REST across the moderate-drift clean-to-messy spectral-gap regimes. DOG×PRISM STOP_OR_REFINE — reciprocal-only also matched REST on simulated PRISM contract-gate classification / false-pass risk while running faster and producing a more stable representation.

## Control docs for this phase
Use these before reopening old phase reports:
- `ROADMAP.md`
- `WORKLOG.md`
- `DECISIONS.md`
- `docs/project-plan/CHAIRMAN_DECISION_TARGET_MEMO_2026-04-13.md`

## Completed decision target
The decisive slice has now been run:
- **Target regime:** moderate-drift synthetic streams with clean-to-messy spectral-gap variation
- **Primary question:** question 2 from the chairman creativity plan
- **Downstream task:** short-horizon online regression plus stability scorecard
- **Baselines:** REST, reciprocal-only, covariance-whitening, no-transform
- **Primary metrics:** stability, downstream error, variance across seeds, runtime cost
- **Result:** PIVOT

## Current execution rule
Prefer small slices that do one of the following, in order:
1. preserve the decision-slice and DOG×PRISM mock evidence,
2. avoid re-litigating current REST vs reciprocal-only unless a genuinely new architecture is introduced,
3. if Sean approves another spike, test one minimal architecture change against both DOG's decision harness and the PRISM contract mock harness,
4. update theorem or method prose only after new evidence exists.

Do **not** broaden scope, revive universal-geometry claims, or polish theorem prose as a substitute for the failed scorecards.

## Priority queue

### 1) Record the pivot implication cleanly
**Why first now:** the benchmark harness, scorecard, and run are complete; the repo needs to treat the PIVOT as real evidence.

**Definition of done:**
- `docs/project-plan/CHAIRMAN_DECISION_SLICE_EVALUATION_NOTE_2026-04-28.md` remains the canonical note,
- `experiments/results/decision_slice_metrics.json` remains the machine-readable evidence,
- future work cites the pivot rather than reopening the same benchmark question.

### 2) Preserve the DOG×PRISM mock stop/refine result
**Why second:** the approved paper/mock collaboration did not rescue current REST; reciprocal-only remained enough on the simulated PRISM contract-gate scorecard.

**Definition of done:**
- `docs/project-plan/DOG_PRISM_ARCHITECTURE_SPIKE_PLAN_2026-04-28.md` remains the companion plan,
- `docs/project-plan/DOG_PRISM_CONTRACT_MOCK_EVALUATION_2026-04-28.md` remains the canonical DOG-owned mock result,
- `experiments/results/prism_contract_mock_metrics.json` remains the machine-readable evidence.

### 3) If Sean approves another spike, test one minimal variant against both harnesses
**Why third:** any pivot follow-up must beat the exact DOG benchmark current REST failed and must not degrade PRISM contract-gate auditability.

**Definition of done:**
- one minimal architecture change is implemented without broad operator-family expansion,
- `run_decision_slice.py` and `run_prism_contract_mock.py` can evaluate it under the same regimes/traces,
- the result is continue / refine / stop for the variant.

### 4) Tighten method / theorem docs only after new variant evidence exists
**Why fourth:** theory alignment should mirror surviving empirical evidence rather than rationalize the failed mainline slice.

**Definition of done:**
- any edits to `REST_METHOD_NOTE.md` or `REST_THEOREM_DRAFT.md` explicitly cite the decision-slice or variant result,
- no new broad framing is introduced.

## Applied stop / continue signal
- **Pivot fired:** reciprocal-only matched or beat REST across the board on the locked scorecard.

## One-sentence guidance for the next stand-up
If there is only one slice to do next, do this:

> do not promote current REST; if Sean wants another attempt, test one minimal architecture change against both the DOG decision slice and the PRISM contract mock harness, with reciprocal-only as the standard to beat.
