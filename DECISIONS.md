# DECISIONS

_Last updated: 2026-04-28_

This file is the compressed decision record for the repo. It is meant to answer: what has already been decided, what remains intentionally deferred, and what should guide the next slices.

## Active decisions

### D1 — Frame REST as a geometric preconditioner
**Decision:** Treat the active contribution as a **covariance-based streaming geometric preconditioner in retained spectral coordinates**, not as a fully established new geometry paradigm or a proven ordering-sensitive mechanism.

**Why:** Phase 4 and Phase 5 established that the current implementation is real and useful enough to study, but the broadest novelty framing is weaker than originally hoped. The preconditioner framing is the strongest honest summary that matches the code and evidence.

**Implications:**
- README, theorem notes, and evaluation summaries should use preconditioner language.
- Avoid broad claims of universal superiority or architecture-independent novelty.
- Prefer disciplined scope over ambitious framing.

### D2 — Keep the covariance-based retained-coordinate implementation as the reference line
**Decision:** The canonical implemented reference remains the covariance-based retained-coordinate path already present in `src/rest/`, but current REST is **not** a validated continuation line after the locked PIVOT result.

**Why:** It is the implemented, tested object that future work must compare against. However, the first decisive scorecard showed reciprocal-only matching or beating current REST, so preserving the implementation is not the same as promoting it.

**Implications:**
- Use the covariance formulation as the default reference point in active docs.
- Do not broaden or continue current REST as-is without new evidence.
- Defer operator-family diversification until a narrow variant beats reciprocal-only under the post-PIVOT protocol.

### D3 — Bound the theory claim to one-step stability / perturbation language
**Decision:** The theorem target is a **single-step perturbation or stability bound** for the retained-coordinate preconditioner under the current assumptions.

**Why:** That is what the current assumptions, diagnostics, and implementation anchors can actually support. The repo does not yet justify claims about long-horizon near-isometry, broad operator-family generality, or a distinct non-commuting ordering effect.

**Implications:**
- Tighten theorem prose and constants around spectral-gap and bounded-weight dependence.
- Keep ordering-based novelty claims out of theorem language unless the architecture changes.
- Treat proof work as alignment and sharpening, not as license to broaden claims.

### D4 — Validate narrowly before expanding outward
**Decision:** Favor narrow, controlled validations in regimes where geometric preconditioning plausibly matters, and explicitly record where simpler transforms still win.

**Why:** Current evidence is synthetic and mixed. That is enough to justify careful follow-up, but not enough to justify a broad real-world campaign.

**Implications:**
- Run targeted sweeps and downstream checks instead of large undirected experiment expansion.
- Document both help-cases and fail-cases.
- Defer broad external validation until theory and contribution framing are tighter.

### D5 — Keep the non-commuting variant as a bounded optional spike
**Decision:** Do **not** make the non-commuting variant the main branch. Keep it as a short, explicit spike only if needed.

**Trigger rule:** Revisit this only if one of the following becomes true:
1. the project still depends on restoring an ordering-sensitive novelty claim,
2. the preconditioner framing proves too weak for the intended paper/note direction, or
3. a simple non-commuting change appears likely to produce distinct behavior without major complexity cost.

**Implications:**
- Main-line work should continue without waiting on this variant.
- If explored, the spike should be time-boxed and judged against clear exit criteria.

### D6 — Maintain project-control docs as first-class repo state
**Decision:** `PROJECT_STATUS.md`, `SETUP.md`, and `DECISIONS.md` are the top-level control layer for the repo and should stay synchronized with the actual code/theory state.

**Why:** Earlier iteration suffered from ambiguity and operational friction. A compressed control layer reduces re-reading cost and makes the next slice obvious.

**Implications:**
- Update these files when scope, blockers, or execution norms materially change.
- Maintain `docs/project-plan/NEXT_ACTIONS.md` as the rolling short queue derived from those decisions.
- Use them to keep future stand-up slices small and resumable.

### D7 — Lock the first decisive validation slice
**Decision:** Execute the authoritative target defined in `docs/project-plan/CHAIRMAN_DECISION_TARGET_MEMO_2026-04-13.md`.

**Locked target:**
- moderate-drift synthetic streams with clean-to-messy spectral-gap variation,
- primary question: whether REST keeps an edge once reciprocal-only is treated as a serious baseline,
- downstream task: short-horizon online regression plus stability scorecard,
- baselines: REST, reciprocal-only, covariance-whitening, and no-transform,
- metrics: stability, downstream error, variance across seeds, runtime cost.

**Result:** complete. See `docs/project-plan/CHAIRMAN_DECISION_SLICE_EVALUATION_NOTE_2026-04-28.md` and `experiments/results/decision_slice_metrics.json`.

### D8 — Treat the locked decision slice as a PIVOT signal
**Decision:** Do not continue the current REST architecture as-is into broader validation. The locked slice produced **PIVOT**: reciprocal-only matched or beat REST across the tested regimes on stability/downstream error and was faster.

**Implications:**
- Mainline expansion is not justified by the first decisive scorecard.
- Theory or method prose should not be polished to rationalize the failed slice.
- Any variant must be judged against the same REST / reciprocal-only / covariance-whitening / no-transform benchmark standard.
- Matching reciprocal-only is not enough to continue; reciprocal-only is now the hard baseline to beat.

### D9 — Make reciprocal-only the hard post-PIVOT baseline
**Decision:** Every next research slice must treat reciprocal-only as the explicit hard baseline. Current REST and any proposed variant must beat reciprocal-only on the pre-registered scorecard to earn continuation.

**Why:** Reciprocal-only has now matched or beaten current REST in the locked DOG decision slice and matched REST on simulated PRISM contract-gate classification / false-pass risk while running faster and producing a more stable representation.

**Implications:**
- `STOP_OR_REFINE` is the default if reciprocal-only remains enough.
- Runtime, stability, downstream error, false-pass rate, and auditability must be reported against reciprocal-only.
- Claims may not compare only against no-transform or whitening when reciprocal-only is the meaningful competitor.

### D10 — Use the post-PIVOT refinement protocol before proposing variants
**Decision:** The controlling protocol for the next bounded DOG slice is `docs/project-plan/POST_PIVOT_REFINEMENT_PROTOCOL_2026-04-28.md`.

**Why:** The repo needs a narrow path for possible architectural refinement without sliding back into theorem-first claim inflation or PRISM-help claims.

**Implications:**
- Test at most one mechanism-specific variant per slice.
- Compare against no-transform, covariance-whitening, reciprocal-only, current REST, and the proposed variant.
- Run both the DOG decision-slice harness and the DOG×PRISM paper/mock harness, or explicitly record why only a smaller reproduction check was feasible.
- No DOG result may claim REST helps PRISM. At most, a future variant may claim a paper/mock contract-gate scorecard improvement if it beats reciprocal-only without worsening false-pass risk or auditability.

### D11 — Treat reciprocal-only robustness sweep as another stop/refine signal
**Decision:** `docs/project-plan/RECIPROCAL_ROBUSTNESS_SWEEP_2026-04-28.md` is the current robustness evidence. Reciprocal-only remains enough under the registered sweep rule.

**Why:** The sweep covered 35 DOG scenario/regime summaries and 4 PRISM mock guardrail scenarios. No REST/whitening/no-transform comparison beat reciprocal-only while also satisfying downstream, stability, runtime, false-pass, and auditability constraints. No-transform produced some downstream-only signals, but failed stability and PRISM false-pass guardrails.

**Implications:**
- Do not treat no-transform downstream-only signals as a REST continuation path.
- Do not promote REST or whitening from this sweep.
- The next evidence-bearing work must either introduce one bounded, pre-registered variant or explicitly reposition the project around reciprocal-only / scope demotion.

## What would justify reopening these decisions
Revisit the current decisions only if one of the following happens:
- theorem tightening materially changes what can be honestly claimed,
- targeted validation reveals a much stronger or weaker empirical picture than Phase 4/5,
- a non-commuting variant demonstrates clearly distinct and worthwhile behavior,
- or the repo is repackaged for a different audience (for example, a paper-first or benchmark-first push).

## Present operating rule
During the post-PIVOT refinement phase, the repo should behave as follows:
1. preserve the PIVOT evidence from the locked decision slice,
2. preserve the DOG×PRISM STOP_OR_REFINE mock evidence,
3. preserve the reciprocal-only robustness sweep result,
4. do not broaden or continue the current REST line as-is,
5. require reciprocal-only as the hard baseline for every new slice,
6. test at most one minimal variant against both the DOG decision harness and the PRISM mock harness,
7. tighten theorem and method notes only after variant evidence exists,
8. keep the control docs current and honest.
