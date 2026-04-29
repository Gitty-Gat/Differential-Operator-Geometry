# PROJECT_STATUS

_Last updated: 2026-04-28_

## Current status
**Post-PIVOT refinement / claim-control program. Current REST is a reference implementation, not a validated continuation claim.**

The repository is no longer in idea-only mode. Phases 1–5 produced:
- a covariance-based REST implementation,
- tests and synthetic experiment scaffolding,
- ablation and downstream-task notes,
- a clearer scope decision,
- and a more honest framing of the current contribution.

The strongest current statement remains:

> REST is presently best understood as a **covariance-based streaming geometric preconditioner in retained spectral coordinates**, with partial one-step stability formalization and controlled synthetic empirical support; however, the locked decision slice produced **PIVOT**, so current REST must not be promoted unless a future variant beats reciprocal-only.

## Current decisive validation result
The prior human-selection blocker was cleared by `docs/project-plan/CHAIRMAN_DECISION_TARGET_MEMO_2026-04-13.md`, and the locked slice was executed on 2026-04-28.

Artifacts:
- `experiments/synthetic/run_decision_slice.py`
- `experiments/results/decision_slice_metrics.json`
- `docs/project-plan/CHAIRMAN_DECISION_SLICE_EVALUATION_NOTE_2026-04-28.md`

Result:
- **PIVOT** — reciprocal-only matched or beat REST across the locked moderate-drift clean-to-messy spectral-gap regimes on stability and downstream error, while also running faster.

## DOG×PRISM paper/mock follow-on result
Approved bounded follow-on artifacts:
- `docs/project-plan/DOG_PRISM_ARCHITECTURE_SPIKE_PLAN_2026-04-28.md`
- `experiments/synthetic/run_prism_contract_mock.py`
- `experiments/results/prism_contract_mock_metrics.json`
- `docs/project-plan/DOG_PRISM_CONTRACT_MOCK_EVALUATION_2026-04-28.md`

Result:
- **STOP_OR_REFINE** — in simulated PRISM theorem-to-contract traces, reciprocal-only matched REST on contract classification and false-pass risk while running faster and producing a more stable representation. No live/write authority was used or widened.

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
- Evidence that current REST is superior to reciprocal-only.
- Any claim that REST helps PRISM.
- Large-scale or real-world benchmark validation.
- Broad operator-family generalization beyond the covariance case.
- Strong claims of general superiority across downstream tasks.

## Canonical project direction
**Decision:** do not continue the current REST architecture as-is without revision; the locked scorecard fired the pivot condition, and the DOG×PRISM mock also returned STOP_OR_REFINE.

Current operating rule:
1. preserve the decision-slice evidence as the canonical benchmark result,
2. preserve the DOG×PRISM mock evidence as paper/mock-only and not a PRISM-help claim,
3. make reciprocal-only the hard baseline for every next research slice,
4. test exactly one minimal variant at a time against both `experiments/synthetic/run_decision_slice.py` and `experiments/synthetic/run_prism_contract_mock.py`,
5. update method/theorem prose only after new evidence exists.

## Highest-priority open work
1. Treat `docs/project-plan/CHAIRMAN_DECISION_SLICE_EVALUATION_NOTE_2026-04-28.md` as the canonical decision note.
2. Treat `docs/project-plan/POST_PIVOT_REFINEMENT_PROTOCOL_2026-04-28.md` as the controlling protocol for any next variant.
3. Do not promote current REST based on the DOG×PRISM mock; it also failed to beat reciprocal-only.
4. Keep REST / reciprocal-only / covariance-whitening / no-transform as the comparison standard, with reciprocal-only as the hard baseline to beat.
5. Avoid broad expansion until a variant or repositioning earns evidence.

## Current blockers / risks
- **Contribution-framing risk:** the original ordering-sensitive novelty story is weakened by commutativity in the active architecture.
- **Theory risk:** proof language can still drift beyond what the current assumptions justify.
- **Evaluation risk:** the current evidence is still controlled and synthetic; external validity is unproven.
- **Execution risk:** the benchmark has now produced a PIVOT; the remaining risk is ignoring that evidence and drifting back into broad framing or theorem polish.

## Read-first map
- `README.md` — repo-level framing.
- `SETUP.md` — exact environment and execution path for tests and synthetic experiments.
- `DECISIONS.md` — compressed record of active scope and locked next-slice rules.
- `docs/project-plan/CHAIRMAN_DECISION_TARGET_MEMO_2026-04-13.md` — authoritative decision target for the completed slice.
- `docs/project-plan/CHAIRMAN_DECISION_SLICE_EVALUATION_NOTE_2026-04-28.md` — canonical PIVOT result from the locked benchmark.
- `docs/project-plan/NEXT_ACTIONS.md` — short operational queue for the next slices.
- `docs/project-plan/POST_PIVOT_REFINEMENT_PROTOCOL_2026-04-28.md` — hard-baseline and claim-control protocol for any next variant.
- `docs/project-plan/PHASE5_COMPLETION_REPORT.md` — what Phase 5 changed.
- `docs/project-plan/PHASE5_SCOPE_DECISION.md` — current strategic scope decision.
- `docs/project-plan/PHASE4_EVALUATION_NOTE.md` — best compact empirical picture before the next slice.

## Practical interpretation
If someone asks what this repo currently is, the best short answer is:

> a disciplined research repo for studying REST as a retained-coordinate streaming geometric preconditioner, now holding a locked PIVOT result showing that current REST did not beat reciprocal-only and that reciprocal-only is the hard baseline for any future variant.

## Repo operations status
- 2026-04-08: the repo is currently synchronized with `origin/main`.
- The earlier SSH/push blocker is no longer the active story and should not be treated as a standing blocker unless it recurs.
- If remote auth fails again in a future slice, record it as a fresh operational blocker rather than preserving stale failure text.

## Control docs to read first
- `ROADMAP.md`
- `WORKLOG.md`
- `docs/project-plan/CHAIRMAN_DECISION_TARGET_MEMO_2026-04-13.md`
- `docs/project-plan/NEXT_ACTIONS.md`
