# NEXT_ACTIONS

_Last updated: 2026-04-13_

This file is the short operational queue for the repo. It exists to turn the current framing into the next few resumable slices without re-reading the entire project history.

## Active objective
Force a clear answer to the locked strategic question:

> Does REST retain a defendable edge in moderate-drift synthetic streams with clean-to-messy spectral-gap variation once reciprocal-only is treated as a serious baseline?

## Control docs for this phase
Use these before reopening old phase reports:
- `ROADMAP.md`
- `WORKLOG.md`
- `DECISIONS.md`
- `docs/project-plan/CHAIRMAN_DECISION_TARGET_MEMO_2026-04-13.md`

## Locked decision target
The next decisive slice is fixed as:
- **Target regime:** moderate-drift synthetic streams with clean-to-messy spectral-gap variation
- **Primary question:** question 2 from the chairman creativity plan
- **Downstream task:** short-horizon online regression plus stability scorecard
- **Baselines:** REST, reciprocal-only, covariance-whitening, no-transform
- **Primary metrics:** stability, downstream error, variance across seeds, runtime cost

## Current execution rule
Prefer small slices that do one of the following, in order:
1. implement the benchmark harness for the locked decision target,
2. define the regime-by-regime scorecard and output schema,
3. run the decisive slice and force a continue / refine / pivot interpretation,
4. update theorem or method prose only after the evidence lands.

Do **not** spend the next slices broadening scope, reviving universal-geometry claims, or exploring the non-commuting variant unless the locked scorecard points there.

## Priority queue

### 1) Build the narrow benchmark harness
**Why first now:** the human decision memo is in hand, so the previous target-selection blocker is gone.

**Definition of done:**
- a runnable script or small command set covers moderate-drift synthetic streams with spectral-gap variation,
- the baseline set includes REST, reciprocal-only, covariance-whitening, and no-transform,
- results are written in a machine-readable schema,
- one compact table or plot can be regenerated from the run.

### 2) Define the regime-by-regime scorecard
**Why second:** the repo needs forced interpretations, not another round of generic artifacts.

**Definition of done:**
- each regime records stability, downstream error, variance across seeds, and runtime cost,
- each regime gets a useful / neutral / negative interpretation,
- the scorecard supports the memo's continue / refine / pivot rule directly.

### 3) Run the decisive validation slice
**Why third:** once the harness and scorecard exist, the repo should cash the decision immediately.

**Definition of done:**
- exact regimes tested are listed,
- win/loss summary versus reciprocal-only is explicit,
- continue / refine / pivot recommendation is stated without hedging,
- artifact paths are recorded in the resulting evaluation note.

### 4) Tighten method / theorem docs only after the result is known
**Why fourth:** theory alignment should mirror the surviving empirical claim rather than substitute for it.

**Definition of done:**
- any edits to `REST_METHOD_NOTE.md` or `REST_THEOREM_DRAFT.md` are directly justified by the decisive slice,
- no new broad framing is introduced.

## Stop / continue signals
- **Continue:** REST wins clearly on at least one meaningful regime without losing badly on runtime.
- **Refine:** results are mixed but show a narrow interpretable niche.
- **Pivot:** reciprocal-only matches or beats REST across the board.

## One-sentence guidance for the next stand-up
If there is only one slice to do next, do this:

> implement and run the locked moderate-drift spectral-gap benchmark slice so the repo gets a real continue / refine / pivot answer instead of another narrative cleanup pass.
