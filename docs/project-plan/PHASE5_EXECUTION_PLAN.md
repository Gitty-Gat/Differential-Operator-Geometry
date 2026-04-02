# PHASE5_EXECUTION_PLAN

## Purpose
Phase 5 is the reframing-and-theory-tightening phase. Phase 4 showed that the current covariance-based retained-coordinate REST implementation is viable, but also exposed a structural limitation: in the present diagonal setting, reciprocal and exponential weighting commute. That means the strongest current version of the project is not an ordering-driven mechanism, but a **streaming geometric preconditioner**.

Phase 5 therefore exists to do three things:
1. reframe the contribution honestly,
2. tighten the theorem draft so it matches the implemented regime,
3. test whether a minimal non-commuting revision is worth further investment.

## Phase 5 objective
At the end of Phase 5, the repository should contain:
1. a consistent preconditioner framing across active formal documents,
2. a tightened one-step stability theorem stated for the actual implemented regime,
3. an explicit decision on whether a non-commuting architectural variant is worth pursuing,
4. a recommendation on whether to broaden to real-world datasets or narrow the scope.

## Workstream A: canonical reframing

### A1. Update active formal documents
The active method and theorem documents should consistently describe REST as:
- a covariance-based retained-coordinate transform,
- a geometric preconditioner,
- and not yet a validated ordering-sensitive mechanism.

### A2. Update repo-facing narrative
README and future summaries should make the current state explicit:
- viable implementation,
- meaningful diagnostics,
- ordering-ablation limitation,
- refine recommendation.

## Workstream B: theorem tightening

### B1. Match theorem scope to implementation
The theorem should be rewritten to target exactly what is implemented:
- covariance PSD setting,
- retained-coordinate transform,
- diagonal composite weight map,
- one-step stability bound,
- bounded gap/drift/clipping regime.

### B2. Remove unsupported emphasis
The theorem note should not imply that the canonical result depends on a non-commuting order effect. In the present implementation, it does not.

### B3. Produce a cleaner proof note
The next theorem draft should:
- sharpen constants where practical,
- separate assumptions clearly,
- align each assumption with a diagnostic already logged in Phase 4,
- and explicitly state the limited interpretation of the result.

## Workstream C: optional non-commuting-variant spike

### C1. Goal
Run one short spike to test whether a non-commuting formulation can restore a genuinely distinguishable ordering effect.

### C2. Candidate directions
Possible minimal variants:
- off-diagonal coupling inserted between reciprocal and exponential maps,
- a graph-Laplacian-based local operator that changes the transform basis or coupling structure,
- a two-basis formulation where flattening and lifting are not both diagonal in the same retained basis.

### C3. Decision rule
Only continue this spike if it produces a genuinely distinguishable ordering effect without destroying stability or interpretability.

## Workstream D: scope decision
After reframing and theorem tightening, make an explicit decision:

1. **Broaden**
   - move toward real-world datasets with the preconditioner framing.
2. **Narrow**
   - focus on regimes where geometric preconditioning clearly helps.
3. **Revise architecture**
   - invest in a non-commuting variant before broader validation.

## Deliverables
Recommended Phase 5 outputs:
- `docs/project-plan/PHASE5_THEORY_ALIGNMENT_NOTE.md`
- `docs/project-plan/PHASE5_NONCOMMUTING_VARIANT_SPIKE.md`
- `docs/project-plan/PHASE5_SCOPE_DECISION.md`
- `docs/project-plan/PHASE5_COMPLETION_REPORT.md`

## Exit condition
Phase 5 is complete only if the repository can answer:
1. What is REST's strongest honest framing right now?
2. What exactly does the current theorem support?
3. Is a non-commuting variant worth pursuing?
4. Should the next investment be broader validation, narrower scope, or architectural revision?

## Conclusion
Phase 5 is the honesty phase. It should reduce overclaiming, increase alignment between theory and code, and determine whether the project should scale as a preconditioner-focused method or change architecture before further growth.
