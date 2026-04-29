# NEXT_ACTIONS

_Last updated: 2026-04-28_

This file is the short operational queue for the repo. It exists to turn the current framing into the next few resumable slices without re-reading the entire project history.

## Active objective
Respond to the locked decision-slice result:

> PIVOT — reciprocal-only matched or beat REST across the moderate-drift clean-to-messy spectral-gap regimes on the locked stability/downstream scorecard, while also running faster.

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
1. preserve the decision-slice evidence and avoid re-litigating the completed benchmark,
2. prepare a bounded architecture-change proposal only if Sean approves pivot follow-up,
3. if approved, test one minimal variant against the exact same decision harness,
4. update theorem or method prose only after variant evidence exists.

Do **not** broaden scope, revive universal-geometry claims, or polish theorem prose as a substitute for the failed locked scorecard.

## Priority queue

### 1) Record the pivot implication cleanly
**Why first now:** the benchmark harness, scorecard, and run are complete; the repo needs to treat the PIVOT as real evidence.

**Definition of done:**
- `docs/project-plan/CHAIRMAN_DECISION_SLICE_EVALUATION_NOTE_2026-04-28.md` remains the canonical note,
- `experiments/results/decision_slice_metrics.json` remains the machine-readable evidence,
- future work cites the pivot rather than reopening the same benchmark question.

### 2) Ask Sean whether to authorize a bounded architecture-change spike
**Why second:** the locked scorecard explicitly points away from continuing current REST as-is.

**Definition of done:**
- Sean approves or rejects spending time on one bounded variant,
- the spike has one entry condition, one command, and one exit decision,
- the same REST / reciprocal-only / whitening / no-transform harness remains the comparison standard.

### 3) If approved, test one minimal variant against the same harness
**Why third:** any pivot follow-up must beat the exact benchmark that current REST failed.

**Definition of done:**
- one minimal architecture change is implemented without broad operator-family expansion,
- `run_decision_slice.py` or a paired script can evaluate it under the same regimes/seeds,
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

> decide whether Sean wants a bounded architecture-change spike; if yes, test one minimal variant against the exact same decision-slice harness rather than broadening the project.
