# PRECONDITIONER POSITIONING NOTE

_Last updated: 2026-04-30_

## Current honest framing
The strongest current contribution in this repo is **not** a general proof that stage ordering creates a distinct computational mechanism, and it is **not** a validated claim that current REST beats reciprocal-only. After the locked PIVOT, robustness sweep, adversarial search, and PRISM↔DOG stand-down, the strongest current contribution is narrower:

> DOG studies retained-coordinate streaming spectral preconditioners, with reciprocal-only as the hard baseline and current evidence-supported center of gravity; current REST is a covariance-based reference implementation for comparison/refinement rather than a validated continuation claim.

## What this means
- The repo studies a concrete operator family rather than a universal geometry-computation thesis.
- The implemented covariance path is the main line, not a placeholder.
- Reciprocal and exponential weighting should currently be understood as commuting diagonal reweightings in the retained-coordinate setting.
- The practical question is whether retained-coordinate preconditioning gives useful behavior in some regimes, with reciprocal-only treated as the minimal core to beat.
- PRISM↔DOG collaboration is stood down unless explicitly reauthorized; prior paper/mock artifacts are archived claim-control evidence only.

## What should not be claimed right now
- That ordering-sensitive novelty is independently established in the active architecture.
- That current REST is validated as superior to reciprocal-only.
- That REST helps PRISM.
- That the current theorem draft proves broad geometric superiority.
- That synthetic results already justify broad real-world performance claims.

## Consequence for method/theory docs
Method and theorem documents inherit this framing: they may preserve current REST as a reference object, but must not use theory language to restart REST promotion, PRISM integration, or claims against reciprocal-only without new benchmark evidence.

## Consequence for execution
The next good slices are:
1. preserve the PIVOT, archived DOG×PRISM STOP_OR_REFINE, robustness, and adversarial evidence,
2. use reciprocal-only as the hard baseline and active positioning center,
3. follow `docs/project-plan/RECIPROCAL_ONLY_CHARACTERIZATION_AND_SCOPE_DEMOTION_2026-04-30.md` before method/theory edits,
4. run one narrow DOG-local benchmark-backed refinement slice at a time only if a genuinely new variant is pre-registered,
5. preserve archived PRISM mock evidence without restarting PRISM integration unless explicitly reauthorized,
6. keep the repo control layer simple and honest.
