# PHASE4_EVALUATION_AND_REFINEMENT_PLAN

## Purpose
Phase 4 is the evaluation-and-refinement phase. Phase 3 established that the canonical covariance-based REST implementation is computationally viable, testable, and empirically distinguishable from simple baselines on controlled synthetic streams. Phase 4 is where the project must determine whether those early signals survive stronger scrutiny.

This phase should not broaden the project recklessly. Its job is to deepen rigor:
- strengthen the experimental story,
- tighten the bridge between the theorem draft and the implementation,
- identify where REST helps,
- identify where REST fails,
- and decide whether the method warrants broader validation or architectural revision.

## Phase 4 objective
At the end of Phase 4, the repository should contain:
1. a stronger empirical evaluation suite,
2. tighter alignment between formal assumptions and implementation choices,
3. richer ablations and parameter-sensitivity studies,
4. at least one controlled downstream-task benchmark,
5. an explicit refinement decision: continue, revise, or narrow the method.

## 1. Core questions Phase 4 must answer
Phase 4 exists to answer the following questions clearly and honestly:
1. Does REST provide a meaningful stability-versus-structure tradeoff beyond simpler baselines?
2. Under what parameter regimes does REST behave well?
3. Under what regimes does REST become fragile or unnecessary?
4. Do the synthetic benefits translate into better behavior on controlled downstream tasks?
5. Are the current reciprocal and exponential design choices justified, or should the formulation be refined before scaling further?

## 2. Workstream A: strengthen empirical rigor

### A1. Expand parameter sweeps
Go beyond the initial beta sweep. Sweep at least:
- `beta`
- `ridge_scale`
- retained rank `k`
- reciprocal clipping bounds
- exponential clipping bounds
- window size

### A2. Record richer metrics
Extend the current metric set to include:
- adjacent-output stability,
- retained-coordinate norm drift,
- spectral-weight sensitivity,
- condition proxies,
- basis-motion diagnostics,
- sensitivity to spectral gap degradation,
- runtime scaling with dimension, rank, and window size.

### A3. Visualization mandate
Phase 4 must generate reproducible visual outputs, not only JSON summaries. At minimum, the experiment runner should save all of the following into `experiments/results/figures/`:
- `stability_vs_beta.*`
- `condition_proxy_heatmap.*`
- `example_embedding_trajectories.*`

The exact extension may vary (`svg`, `png`, etc.), but the figure types are mandatory.

## 3. Workstream B: deepen ablation logic

### B1. Ordered-composition ablation
The central novelty candidate is the ordered reciprocal-then-exponential composition. Phase 4 must test whether this ordering matters.

Required variants:
1. raw retained coordinates,
2. reciprocal-only,
3. exponential-only,
4. reciprocal-then-exponential (REST canonical),
5. exponential-then-reciprocal (ordering ablation).

### B2. Functional-form ablation
Test whether the current transform laws are doing real work or merely one convenient instantiation.

Examples:
- reciprocal exponent `-1/2` versus stronger/weaker reciprocal forms,
- alternative shaping functions `phi`,
- alternative clipped exponential gain schedules,
- fixed versus adaptive ridge scale.

### B3. Failure-mode probe
Add an explicit fourth synthetic family designed to stress where REST fails.

Examples:
- extreme sparsity,
- high noise,
- rapidly collapsing spectral gap,
- over-large `beta`,
- too-small ridge scale,
- overly aggressive clipping.

This probe must be documented explicitly in the evaluation note rather than treated as an incidental run.

## 4. Workstream C: connect theory draft to implementation

### C1. Map assumptions to code
For each formal assumption from `REST_THEOREM_DRAFT.md`, identify the matching implementation control:
- PSD operator -> covariance construction,
- bounded drift -> experiment design,
- spectral gap -> monitored diagnostic,
- bounded transform laws -> clipping,
- bounded ridge scale -> parameter policy.

### C2. Add assumption diagnostics
Implementation should log or estimate:
- retained spectral gap over time,
- drift `||L_t - L_{t-1}||_2` or a practical proxy,
- whether clipping is active and how often,
- how basis motion behaves under the current stream.

### C3. Tighten theorem-to-experiment traceability
Phase 4 should produce a note explicitly stating:
- which experiments approximately satisfy the theorem assumptions,
- which do not,
- and where empirical behavior diverges from the theorem's intended regime.

## 5. Workstream D: introduce controlled downstream tasks
Phase 3 deliberately stayed mostly structural. Phase 4 should add at least one downstream-task layer while keeping the tasks controlled and interpretable.

### Recommended tasks
1. **Change-point or anomaly sensitivity**
2. **Simple clustering on streaming segments**
3. **Short-horizon regression or forecasting proxy**

### Rule
Do not jump to complex application domains yet. Keep the tasks synthetic or tightly controlled so conclusions remain attributable to the representation, not to dataset messiness.

## 6. Quantitative success thresholds
The Phase 4 evaluation note must define lightweight pass/fail bars. Recommended thresholds:

1. **Stability threshold**
   - REST stability within 10% of the best ablation on at least 2 of 3 primary drift families.
2. **Conditioning threshold**
   - at least one `beta` regime with mean condition proxy < 2.0 while REST stability remains below a moderate instability threshold.
3. **Failure-probe threshold**
   - explicit documentation of at least one regime where REST underperforms a simpler baseline.
4. **Downstream threshold**
   - REST should place competitively on at least one controlled downstream benchmark family.

These thresholds are not publication claims. They are internal decision aids.

## 7. Workstream E: decide whether to refine the method
Phase 4 is not only about validating REST. It is also about deciding whether the current form of REST is the right form.

### Questions to decide
- Is the covariance-based formulation sufficient to justify further work?
- Is the reciprocal operator too conservative or too aggressive?
- Is the exponential lift helping enough to justify its complexity?
- Should `beta` remain fixed, or become adaptive?
- Is the method strongest as a geometric preconditioner rather than a general representation method?

### Possible outcomes
1. **Continue as-is**
2. **Refine the transform laws**
3. **Narrow the scope**
4. **Reframe the contribution**

## 8. Deliverables for Phase 4
By the end of Phase 4, the repository should contain at least:
- an expanded experiment runner,
- richer metrics and visualization outputs,
- a downstream-task benchmark note,
- an ablation note or ablation section in the evaluation note,
- a theorem-to-experiment traceability note,
- a Phase 4 completion report,
- and a Phase 5 recommendation memo.

Recommended file targets:
- `docs/project-plan/PHASE4_EVALUATION_NOTE.md`
- `docs/project-plan/PHASE4_DOWNSTREAM_TASK_NOTE.md`
- `docs/project-plan/PHASE4_THEORY_TO_EXPERIMENT_TRACEABILITY.md`
- `docs/project-plan/PHASE4_COMPLETION_REPORT.md`
- `docs/project-plan/PHASE5_RECOMMENDATION_MEMO.md`

## 9. Decision rubric mandate
The Phase 4 evaluation note must end with a one-page **Go / Refine / Pivot** rubric keyed directly to the five core exit questions. The recommendation should be explicit and traceable to the threshold outcomes.

## 10. What Phase 4 should avoid
To keep the project disciplined, Phase 4 should avoid:
- introducing graph/Jacobian variants before the covariance case is fully stress-tested,
- claiming strong empirical superiority from narrow synthetic wins,
- using noisy real-world datasets too early,
- broadening DOG philosophically without matching evidence,
- adding learned/neural variants before deterministic behavior is understood.

## 11. Exit condition into Phase 5
Phase 4 is complete only if the repository can answer:
1. Where does REST help?
2. Where does REST fail?
3. Which parts of the transform actually matter?
4. How tightly do implementation results match the intended theory regime?
5. Is the method strong enough to scale to broader validation, or does it require architectural refinement first?

## Conclusion
Phase 4 is the seriousness test. Phase 3 showed that REST can be built and run. Phase 4 must show whether the method stands up to disciplined scrutiny, richer ablations, controlled downstream evaluation, explicit thresholds, and an honest go/refine/pivot recommendation.
