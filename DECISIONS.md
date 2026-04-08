# DECISIONS

_Last updated: 2026-04-08_

This file is the compressed decision record for the repo. It is meant to answer: what has already been decided, what remains intentionally deferred, and what should guide the next slices.

## Active decisions

### D1 — Frame REST as a geometric preconditioner
**Decision:** Treat the active contribution as a **covariance-based streaming geometric preconditioner in retained spectral coordinates**, not as a fully established new geometry paradigm or a proven ordering-sensitive mechanism.

**Why:** Phase 4 and Phase 5 established that the current implementation is real and useful enough to study, but the broadest novelty framing is weaker than originally hoped. The preconditioner framing is the strongest honest summary that matches the code and evidence.

**Implications:**
- README, theorem notes, and evaluation summaries should use preconditioner language.
- Avoid broad claims of universal superiority or architecture-independent novelty.
- Prefer disciplined scope over ambitious framing.

### D2 — Keep the covariance-based retained-coordinate implementation as the main line
**Decision:** The canonical active implementation remains the covariance-based retained-coordinate path already present in `src/rest/`.

**Why:** It is the part of the project that is implemented, tested, and tied to current synthetic evidence. Broadening to other operator families now would increase scope faster than confidence.

**Implications:**
- Use the covariance formulation as the default reference point in active docs.
- Defer operator-family diversification until the current line is tighter.

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

## What would justify reopening these decisions
Revisit the current decisions only if one of the following happens:
- theorem tightening materially changes what can be honestly claimed,
- targeted validation reveals a much stronger or weaker empirical picture than Phase 4/5,
- a non-commuting variant demonstrates clearly distinct and worthwhile behavior,
- or the repo is repackaged for a different audience (for example, a paper-first or benchmark-first push).

## Present operating rule
Until new evidence arrives, the repo should behave as follows:
1. keep the covariance-based preconditioner implementation as the main line,
2. tighten theorem and method notes to match that line exactly,
3. run only narrow validation that clarifies where REST helps,
4. defer broad expansion and architecture branching,
5. keep the control docs current and honest.
