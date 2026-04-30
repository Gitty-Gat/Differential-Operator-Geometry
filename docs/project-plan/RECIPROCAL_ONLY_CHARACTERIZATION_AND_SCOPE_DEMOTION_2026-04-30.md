# Reciprocal-Only Characterization and REST Scope Demotion — 2026-04-30

## Status
Active DOG-local positioning note after the locked PIVOT result, reciprocal-only robustness sweep, adversarial failure search, and PRISM↔DOG stand-down.

This note is not new theorem evidence and does not introduce a new architecture. It records the current evidence-supported interpretation so future work does not spend cycles rescuing current REST without a genuinely new pre-registered variant.

## Evidence base
- Locked decision slice: `docs/project-plan/CHAIRMAN_DECISION_SLICE_EVALUATION_NOTE_2026-04-28.md`
- Robustness sweep: `docs/project-plan/RECIPROCAL_ROBUSTNESS_SWEEP_2026-04-28.md`
- Adversarial search: `docs/project-plan/RECIPROCAL_ADVERSARIAL_FAILURE_SEARCH_2026-04-28.md`
- PRISM↔DOG stand-down: `docs/project-plan/PRISM_DOG_STANDDOWN_2026-04-30.md`

## Main conclusion
Reciprocal-only is no longer just a baseline. It is the current evidence-supported center of gravity for the DOG repo.

Current REST remains useful as:
- a reference implementation of the retained-coordinate covariance preconditioner line;
- a comparison method for future bounded variants;
- a source of implementation/theory lessons about commutative diagonal weighting;
- a warning against broad geometry-first claims unsupported by the scorecards.

Current REST does **not** currently earn:
- a mainline continuation claim;
- a superiority claim over reciprocal-only;
- an ordering-sensitive novelty claim in the active diagonal retained-coordinate architecture;
- a PRISM-facing claim.

## What reciprocal-only appears to buy
Across the completed DOG evidence, reciprocal-only is attractive because it is:
- simple and inspectable;
- fast relative to current REST;
- stable across the locked decision-slice regimes;
- competitive or better on downstream error;
- hard for current REST, whitening, or no-transform to beat under registered scorecards.

In the locked decision slice, REST was nearly tied on downstream error but consistently worse on stability and slower than reciprocal-only:

| Regime | REST / reciprocal downstream error | REST / reciprocal stability | Interpretation |
| --- | ---: | ---: | --- |
| clean_gap | 0.992933 | 1.628387 | downstream near-tie, worse stability |
| medium_gap | 1.000134 | 1.599447 | downstream tie/slightly worse, worse stability |
| messy_gap | 0.998613 | 1.553411 | downstream near-tie, worse stability |

The scorecard decision was **PIVOT** because reciprocal-only matched or beat REST across the locked regimes while running faster.

## What reciprocal-only does not solve
The adversarial search found four narrow reciprocal-only downstream failure flags:

| Case | Reciprocal normalized MSE | Reciprocal stability | Failure flag |
| --- | ---: | ---: | --- |
| switching_lag | 1.016386 | 1.070927 | absolute downstream failure |
| outlier_bursts | 1.023815 | 1.090509 | absolute downstream failure |
| low_variance_target | 1.005505 | 1.164468 | absolute downstream failure |
| eigenvalue_collapse | 1.009409 | 0.876737 | absolute downstream failure |

These failures should be treated as baseline characterization, not as REST validation. The same search found no current DOG-side rescue candidate among REST, covariance-whitening, or no-transform.

## Scope demotion
The honest repo framing is now:

> DOG studies retained-coordinate spectral preconditioning behavior in streaming covariance settings, with reciprocal-only as the current hard baseline and likely minimal useful core. Current REST is preserved as a reference implementation and historical research line, not as a validated improvement over reciprocal-only.

This demotes the project from “REST as a promoted method” to “DOG as a disciplined characterization of retained-coordinate streaming preconditioners, currently centered on reciprocal-only.”

## Forward rule
Before any additional architecture work, require one of:

1. **Scope-demotion path:** update method/theory prose around reciprocal-only characterization and stop implying current REST continuation.
2. **New-variant path:** pre-register one minimal DOG-local variant with a specific mechanism that plausibly addresses a named reciprocal-only failure case, then test it against reciprocal-only, current REST, covariance-whitening, and no-transform.

Do not reopen PRISM integration, broad benchmark expansion, or theorem polishing as substitutes for this choice.

## DOG-local acceptance criteria for any future variant
A future variant earns continuation only if it:
- beats reciprocal-only on the pre-registered downstream task;
- does not worsen stability materially;
- has a defensible runtime cost;
- preserves auditability/reconstructability relevant to the DOG-local task;
- is tested against current REST, reciprocal-only, covariance-whitening, and no-transform;
- states whether the result is `CONTINUE_VARIANT`, `REFINE_VARIANT`, or `STOP_OR_REFINE`.

## Immediate next edits suggested
- Tighten `docs/project-plan/REST_METHOD_NOTE.md` so current REST is described as reference architecture, not promoted method.
- Tighten `docs/project-plan/REST_THEOREM_DRAFT.md` only to remove over-claiming; do not add theorem ambition.
- Keep `experiments/synthetic/run_prism_contract_mock.py` archived and reproducible, but out of the default forward plan unless explicitly reauthorized.
