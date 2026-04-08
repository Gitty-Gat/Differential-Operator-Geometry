# PROJECT_STATUS

_Last updated: 2026-04-08_

## Current status
**Active, narrowed research program.**

The repository is no longer in idea-only mode. Phases 1–5 have produced:
- a covariance-based REST implementation,
- tests and synthetic experiment scaffolding,
- ablation and downstream-task notes,
- a clearer scope decision,
- and a more honest framing of the current contribution.

The strongest current statement is:

> REST is presently best understood as a **covariance-based streaming geometric preconditioner in retained spectral coordinates**, with partial one-step stability formalization and controlled synthetic empirical support.

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
**Decision:** narrow and refine before broadening.

Current operating rule:
1. keep the covariance-based implementation as the main line,
2. continue with the geometric-preconditioner framing,
3. tighten theorem language and constants so docs match the code,
4. run only narrow additional validation where preconditioning plausibly matters,
5. treat the non-commuting variant only as a bounded optional spike.

## Highest-priority open work
1. Tighten `docs/project-plan/REST_METHOD_NOTE.md` so assumptions, notation, and claims match the revised theorem framing and implementation reality.
2. Review `docs/project-plan/REST_THEOREM_DRAFT.md` only for proof-detail sharpening or constant cleanup; keep the framing narrow.
3. Use `docs/project-plan/NEXT_ACTIONS.md` as the short operational queue for the next slices.
4. Run narrow follow-up validation focused on where geometric preconditioning helps versus where simpler transforms still win.
5. Revisit the non-commuting variant only if the bounded spike triggers in `DECISIONS.md` are met.

## Current blockers / risks
- **Contribution-framing risk:** the original ordering-sensitive novelty story is weakened by commutativity in the active architecture.
- **Theory risk:** proof language can still drift beyond what the current assumptions justify.
- **Evaluation risk:** current evidence is controlled and synthetic; external validity is still unproven.
- **Project-friction risk:** setup/path/push friction has already slowed iteration and should be reduced via explicit control docs.

## Read-first map
- `README.md` — current repo-level framing.
- `SETUP.md` — exact environment and execution path for tests and synthetic experiments.
- `DECISIONS.md` — compressed record of the active scope, framing, and defer decisions.
- `docs/project-plan/NEXT_ACTIONS.md` — short operational queue for the next slices.
- `docs/project-plan/PHASE5_COMPLETION_REPORT.md` — what Phase 5 changed.
- `docs/project-plan/PHASE5_SCOPE_DECISION.md` — current strategic scope decision.
- `docs/project-plan/PHASE5_THEORY_ALIGNMENT_NOTE.md` — strongest honest theorem framing.
- `docs/project-plan/PHASE4_EVALUATION_NOTE.md` — best compact empirical picture.

## Practical interpretation
If someone asks what this repo currently is, the best short answer is:

> a disciplined research repo for studying REST as a retained-coordinate streaming geometric preconditioner, with narrower claims than originally envisioned and a clear need for theory tightening plus targeted validation.

## Repo operations blocker
- 2026-04-08: `git push origin main` has repeatedly failed with `git@github.com: Permission denied (publickey).`
- The repo includes newer local theory/control-doc updates that may remain committed locally until auth is fixed.
- Do **not** claim remote sync until GitHub SSH credentials or the remote auth method are fixed and a push succeeds.
