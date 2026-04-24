# PROJECT_STATUS

_Last updated: 2026-04-13_

## Current status
**Active, narrowed research program with the next decision slice now locked.**

The repository is no longer in idea-only mode. Phases 1–5 produced:
- a covariance-based REST implementation,
- tests and synthetic experiment scaffolding,
- ablation and downstream-task notes,
- a clearer scope decision,
- and a more honest framing of the current contribution.

The strongest current statement remains:

> REST is presently best understood as a **covariance-based streaming geometric preconditioner in retained spectral coordinates**, with partial one-step stability formalization and controlled synthetic empirical support.

## Current decisive validation target
The prior human-selection blocker is now cleared by `docs/project-plan/CHAIRMAN_DECISION_TARGET_MEMO_2026-04-13.md`.

The next cycle is fixed to:
- **target regime:** moderate-drift synthetic streams with clean-to-messy spectral-gap variation,
- **primary question:** whether REST keeps an edge once reciprocal-only is treated as a serious baseline,
- **downstream task:** short-horizon online regression plus a stability scorecard,
- **baselines:** REST, reciprocal-only, covariance-whitening, and no-transform,
- **primary metrics:** stability, downstream error, variance across seeds, runtime cost,
- **decision rule:** continue / refine / pivot exactly as defined in the memo.

## What is currently supported

### Implementation
- Active code exists under `src/rest/` with supporting baselines and experiments.
- The current canonical path is the covariance-based retained-coordinate implementation.
- The repo includes synthetic evaluation artifacts and generated figures under `experiments/results/`.

### Theory
- The theorem target is a **single-step perturbation / stability bound** for the retained-coordinate preconditioner.
- The theorem draft should be read as preconditioner-focused, not as proof of a distinct ordering-sensitive mechanism.
- Assumption anchors currently available in the repo include PSD covariance construction, retained spectral coordinates, bounded weight maps, and spectral-gap diagnostics.

### Empirical evidence
- Phase 3 established that REST is implementable and testable.
- Phase 4 established mixed-but-real viability under controlled synthetic drift.
- REST is empirically distinguishable from simple baselines, but it is **not** uniformly best.
- Reciprocal-only behavior can outperform REST in some regimes.
- In the current retained-coordinate diagonal formulation, reciprocal and exponential weighting commute, so reversed-order ablations are algebraically identical.

## What is not yet supported
- A completed proof beyond draft level.
- A justified claim that stage ordering is independently meaningful in the current architecture.
- Large-scale or real-world benchmark validation.
- Broad operator-family generalization beyond the covariance case.
- Strong claims of general superiority across downstream tasks.

## Canonical project direction
**Decision:** keep the covariance-based main line, but make the next cycle decision-led rather than wording-led.

Current operating rule:
1. keep the covariance-based implementation as the main line,
2. execute the locked decisive validation slice,
3. benchmark against reciprocal-only, covariance-whitening, and no-transform,
4. judge the result by stability, downstream error, variance across seeds, and runtime cost,
5. only then tighten theorem and method prose to match the surviving claim.

## Highest-priority open work
1. Build the narrow benchmark harness for moderate-drift synthetic streams with controlled spectral-gap variation.
2. Add the regime-by-regime scorecard covering stability, downstream error, variance across seeds, and runtime cost.
3. Run the decisive validation slice and write a compact continue / refine / pivot note.
4. Update `docs/project-plan/REST_METHOD_NOTE.md` and `docs/project-plan/REST_THEOREM_DRAFT.md` only after the new evidence is in hand.
5. Revisit the non-commuting variant only if the locked scorecard triggers a refine/pivot discussion.

## Current blockers / risks
- **Contribution-framing risk:** the original ordering-sensitive novelty story is weakened by commutativity in the active architecture.
- **Theory risk:** proof language can still drift beyond what the current assumptions justify.
- **Evaluation risk:** the current evidence is still controlled and synthetic; external validity is unproven.
- **Execution risk:** the target-selection blocker is cleared, so the remaining risk is failure to implement and interpret the locked benchmark slice cleanly.

## Read-first map
- `README.md` — repo-level framing.
- `SETUP.md` — exact environment and execution path for tests and synthetic experiments.
- `DECISIONS.md` — compressed record of active scope and locked next-slice rules.
- `docs/project-plan/CHAIRMAN_DECISION_TARGET_MEMO_2026-04-13.md` — authoritative decision target for the next cycle.
- `docs/project-plan/NEXT_ACTIONS.md` — short operational queue for the next slices.
- `docs/project-plan/PHASE5_COMPLETION_REPORT.md` — what Phase 5 changed.
- `docs/project-plan/PHASE5_SCOPE_DECISION.md` — current strategic scope decision.
- `docs/project-plan/PHASE4_EVALUATION_NOTE.md` — best compact empirical picture before the next slice.

## Practical interpretation
If someone asks what this repo currently is, the best short answer is:

> a disciplined research repo for studying REST as a retained-coordinate streaming geometric preconditioner, now pointed at one fixed decisive validation slice instead of another round of open-ended framing work.

## Repo operations status
- 2026-04-08: the repo is currently synchronized with `origin/main`.
- The earlier SSH/push blocker is no longer the active story and should not be treated as a standing blocker unless it recurs.
- If remote auth fails again in a future slice, record it as a fresh operational blocker rather than preserving stale failure text.

## Control docs to read first
- `ROADMAP.md`
- `WORKLOG.md`
- `docs/project-plan/CHAIRMAN_DECISION_TARGET_MEMO_2026-04-13.md`
- `docs/project-plan/NEXT_ACTIONS.md`
