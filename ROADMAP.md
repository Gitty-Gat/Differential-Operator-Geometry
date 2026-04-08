# ROADMAP

_Last updated: 2026-04-08_

This roadmap keeps the DOG repo pointed at the narrow honest contribution instead of drifting back into broad geometry-for-everything claims.

## Current phase
**Refine the retained-coordinate preconditioner framing and validate it narrowly.**

## Now
1. Keep REST framed as a covariance-based streaming geometric preconditioner in retained spectral coordinates.
2. Tighten `docs/project-plan/REST_METHOD_NOTE.md` so it matches the theorem draft and the implemented code path.
3. Keep `docs/project-plan/REST_THEOREM_DRAFT.md` narrow: one-step stability, explicit assumptions, no overclaim about ordering-sensitive novelty.
4. Design one small follow-up validation where preconditioning might plausibly matter.

## Next
1. Run one bounded validation slice tied to a single clearly stated question.
2. Record a compact empirical note on when REST helps, when it ties, and when simpler weighting wins.
3. Revisit the non-commuting variant only if the current framing becomes strategically exhausted.

## Not now
- Broad real-world benchmark expansion.
- Sweeping theorem generalization beyond the current covariance setting.
- Repo churn that does not improve theory clarity, validation quality, or operator honesty.
