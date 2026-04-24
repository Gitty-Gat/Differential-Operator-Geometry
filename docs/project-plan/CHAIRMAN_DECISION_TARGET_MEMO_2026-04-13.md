# CHAIRMAN_DECISION_TARGET_MEMO_2026-04-13

## Status
**Authoritative human decision received.** This memo resolves the earlier target-selection blocker for the next DOG cycle.

## Locked decision
The next decisive validation slice is fixed as follows:

- **Target regime:** moderate-drift synthetic streams with clean-to-messy spectral-gap variation
- **Primary question:** Question 2 from the creativity trajectory plan — does REST retain an edge once reciprocal-only is included seriously?
- **Downstream task:** short-horizon online regression plus a stability scorecard
- **Baselines:** REST, reciprocal-only, covariance-whitening, and no-transform
- **Primary metrics:** stability, downstream error, variance across seeds, runtime cost

## Decision rule
- **Continue:** REST wins clearly on at least one meaningful regime without losing badly on runtime.
- **Refine:** results are mixed but show a narrow interpretable niche.
- **Pivot:** reciprocal-only matches or beats REST across the board.

## Operational implication
Priority 0 in `CHAIRMAN_CREATIVITY_TRAJECTORY_IMPLEMENTATION_PLAN_2026-04-13.md` is now complete. The next autonomous work should be:
1. implement the narrow benchmark harness for this slice,
2. define the regime-by-regime scorecard around the locked metrics,
3. run the validation and record a continue/refine/pivot recommendation.
