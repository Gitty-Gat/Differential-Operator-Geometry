# PROJECT_STATUS

_Last updated: 2026-04-30_

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

## DOG×PRISM paper/mock follow-on result — archived / stood down
Archived bounded follow-on artifacts:
- `docs/project-plan/DOG_PRISM_ARCHITECTURE_SPIKE_PLAN_2026-04-28.md`
- `experiments/synthetic/run_prism_contract_mock.py`
- `experiments/results/prism_contract_mock_metrics.json`
- `docs/project-plan/DOG_PRISM_CONTRACT_MOCK_EVALUATION_2026-04-28.md`

Result:
- **STOP_OR_REFINE** — in simulated PRISM theorem-to-contract traces, reciprocal-only matched REST on contract classification and false-pass risk while running faster and producing a more stable representation. No live/write authority was used or widened.

Stand-down:
- As of 2026-04-30, PRISM↔DOG collaboration is no longer active. Preserve these artifacts as historical claim-control evidence, but do not spend DOG cycles on PRISM integration or PRISM-specific guardrail expansion unless explicitly reauthorized. See `docs/project-plan/PRISM_DOG_STANDDOWN_2026-04-30.md`.

## Reciprocal-only robustness / failure-regime sweep
Post-PIVOT evidence artifacts:
- `experiments/synthetic/run_reciprocal_robustness_sweep.py`
- `experiments/results/reciprocal_robustness_sweep_metrics.json`
- `docs/project-plan/RECIPROCAL_ROBUSTNESS_SWEEP_2026-04-28.md`

Result:
- **RECIPROCAL_BASELINE_REMAINS_ENOUGH** — across 35 DOG scenario/regime summaries plus 4 PRISM mock guardrail scenarios, no REST/whitening/no-transform comparison beat reciprocal-only under the registered downstream, stability, runtime, false-pass, and auditability rule. Some no-transform downstream-only signals appeared, but they failed stability and PRISM false-pass guardrails.

## Reciprocal-only adversarial failure search
Adversarial evidence artifacts:
- `experiments/synthetic/run_reciprocal_adversarial_search.py`
- `experiments/results/reciprocal_adversarial_search_metrics.json`
- `docs/project-plan/RECIPROCAL_ADVERSARIAL_FAILURE_SEARCH_2026-04-28.md`

Result:
- **FAILURES_FOUND_NO_DOG_RESCUE** — four narrow synthetic adversarial cases flagged reciprocal-only absolute downstream normalized-MSE failures, but no current REST/whitening/no-transform path beat reciprocal-only while preserving PRISM false-pass and auditability guardrails. Recommendation: stop trying to rescue current REST; refocus on reciprocal-only characterization, scope demotion, or a separately pre-registered new variant only.

## Reciprocal-only characterization / REST scope demotion
Positioning artifact:
- `docs/project-plan/RECIPROCAL_ONLY_CHARACTERIZATION_AND_SCOPE_DEMOTION_2026-04-30.md`

Result:
- Reciprocal-only is the current evidence-supported center of gravity. Current REST is preserved as a reference implementation and comparison method, but it is demoted from promoted method to historical/reference line unless a genuinely new pre-registered DOG-local variant beats reciprocal-only.

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
**Decision:** do not continue the current REST architecture as-is without revision; the locked scorecard fired the pivot condition, the archived DOG×PRISM mock returned STOP_OR_REFINE, and later robustness/adversarial sweeps did not rescue current REST.

Current operating rule:
1. preserve the decision-slice evidence as the canonical benchmark result,
2. preserve the DOG×PRISM mock evidence as archived paper/mock claim-control material only,
3. follow the 2026-04-30 PRISM↔DOG stand-down unless explicitly reauthorized,
4. make reciprocal-only the hard baseline for every next research slice,
5. test exactly one minimal variant at a time against DOG-local decision / robustness / adversarial harnesses,
6. update method/theorem prose only after new evidence exists.

## Highest-priority open work
1. Treat `docs/project-plan/CHAIRMAN_DECISION_SLICE_EVALUATION_NOTE_2026-04-28.md` as the canonical decision note.
2. Treat `docs/project-plan/PRISM_DOG_STANDDOWN_2026-04-30.md` as the active coordination boundary.
3. Treat `docs/project-plan/POST_PIVOT_REFINEMENT_PROTOCOL_2026-04-28.md` as the DOG-local claim-control protocol for any next variant.
4. Treat `docs/project-plan/RECIPROCAL_ROBUSTNESS_SWEEP_2026-04-28.md` as the current robustness result: reciprocal-only remains enough.
5. Treat `docs/project-plan/RECIPROCAL_ADVERSARIAL_FAILURE_SEARCH_2026-04-28.md` as the current adversarial result: failures found, no DOG rescue.
6. Do not promote current REST based on the archived DOG×PRISM mock, robustness sweep, or adversarial search.
7. Keep REST / reciprocal-only / covariance-whitening / no-transform as the comparison standard, with reciprocal-only as the hard baseline to beat.
8. Treat `docs/project-plan/RECIPROCAL_ONLY_CHARACTERIZATION_AND_SCOPE_DEMOTION_2026-04-30.md` as the current positioning note.
9. Avoid broad expansion until a variant or repositioning earns evidence.

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
- `docs/project-plan/PRISM_DOG_STANDDOWN_2026-04-30.md` — active rule standing down PRISM↔DOG collaboration.
- `docs/project-plan/POST_PIVOT_REFINEMENT_PROTOCOL_2026-04-28.md` — hard-baseline and DOG-local claim-control protocol for any next variant.
- `docs/project-plan/RECIPROCAL_ROBUSTNESS_SWEEP_2026-04-28.md` — robustness sweep showing reciprocal-only remains enough under the registered guardrails.
- `docs/project-plan/RECIPROCAL_ADVERSARIAL_FAILURE_SEARCH_2026-04-28.md` — adversarial search showing reciprocal-only failures but no current DOG rescue.
- `docs/project-plan/RECIPROCAL_ONLY_CHARACTERIZATION_AND_SCOPE_DEMOTION_2026-04-30.md` — active positioning note centering reciprocal-only and demoting current REST.
- `docs/project-plan/PHASE5_COMPLETION_REPORT.md` — what Phase 5 changed.
- `docs/project-plan/PHASE5_SCOPE_DECISION.md` — current strategic scope decision.
- `docs/project-plan/PHASE4_EVALUATION_NOTE.md` — best compact empirical picture before the next slice.

## Practical interpretation
If someone asks what this repo currently is, the best short answer is:

> a disciplined research repo for characterizing retained-coordinate streaming preconditioners, now centered on reciprocal-only as the hard baseline, with current REST preserved as a reference implementation after PIVOT / robustness / adversarial evidence failed to rescue it.

## Repo operations status
- 2026-04-08: the repo is currently synchronized with `origin/main`.
- The earlier SSH/push blocker is no longer the active story and should not be treated as a standing blocker unless it recurs.
- If remote auth fails again in a future slice, record it as a fresh operational blocker rather than preserving stale failure text.

## Control docs to read first
- `ROADMAP.md`
- `WORKLOG.md`
- `docs/project-plan/CHAIRMAN_DECISION_TARGET_MEMO_2026-04-13.md`
- `docs/project-plan/NEXT_ACTIONS.md`
