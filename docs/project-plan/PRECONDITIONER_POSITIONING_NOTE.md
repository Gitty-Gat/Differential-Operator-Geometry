# PRECONDITIONER POSITIONING NOTE

_Last updated: 2026-04-28_

## Current honest framing
The strongest current contribution in this repo is **not** a general proof that stage ordering creates a distinct computational mechanism, and it is **not** a validated claim that current REST beats reciprocal-only. The strongest current contribution is narrower:

> REST is a covariance-based streaming geometric preconditioner in retained spectral coordinates, with a partial one-step stability story and controlled synthetic support; after the locked decision slice, current REST is a reference implementation for refinement rather than a validated continuation claim.

## What this means
- The repo studies a concrete operator family rather than a universal geometry-computation thesis.
- The implemented covariance path is the main line, not a placeholder.
- Reciprocal and exponential weighting should currently be understood as commuting diagonal reweightings in the retained-coordinate setting.
- The practical question is whether that preconditioning view gives useful behavior in some regimes, not whether it wins everywhere.

## What should not be claimed right now
- That ordering-sensitive novelty is independently established in the active architecture.
- That current REST is validated as superior to reciprocal-only.
- That REST helps PRISM.
- That the current theorem draft proves broad geometric superiority.
- That synthetic results already justify broad real-world performance claims.

## Consequence for execution
The next good slices are:
1. preserve the PIVOT and DOG×PRISM STOP_OR_REFINE evidence,
2. use reciprocal-only as the hard baseline for any variant,
3. run one narrow benchmark-backed refinement slice at a time,
4. keep PRISM contract obligations auditable in paper/mock work,
5. keep the repo control layer simple and honest.
