# PHASE3_IMPLEMENTATION_PLAN

## Purpose
Phase 3 is the implementation and validation phase. Its role is to take the formal Phase 2 REST specification and build the smallest correct experimental harness needed to test whether the method earns its complexity.

Phase 3 should not expand the theory aggressively. It should operationalize the Phase 2 formulation exactly enough to answer whether REST behaves usefully on controlled streaming problems.

## Phase 3 objective
At the end of Phase 3, the repository should contain:
1. a minimal implementation of covariance-based retained-coordinate REST,
2. synthetic streaming data generators,
3. baseline comparators,
4. reproducible experiment scripts or notebooks,
5. a first empirical evaluation note.

## 1. Implementation scope
The implementation should remain faithful to the canonical Phase 2 setting:
- streaming observations in `\mathbb{R}^d`,
- sliding-window covariance operator `L_t`,
- retained rank `k`,
- reciprocal flattening followed by exponential lifting,
- retained-coordinate output `z_t`.

No graph-based or Jacobian-based variants should be added until the covariance case is functioning and benchmarked.

## 2. Required code artifacts
Recommended Phase 3 repository outputs:
- `src/rest/` or equivalent module for the core transform,
- `src/baselines/` for baseline methods,
- `experiments/synthetic/` for synthetic data experiments,
- `tests/` covering the core transform and basic invariants,
- an experiment results note under `docs/project-plan/` or `experiments/results/`.

## 3. Core implementation tasks

### Task A: streaming covariance operator
Implement:
- sliding-window mean updates,
- sliding-window covariance construction,
- optional numerically stable recomputation checks.

### Task B: retained eigendecomposition
Implement:
- top-`k` eigendecomposition extraction,
- deterministic sorting / sign conventions where needed,
- clear handling of rank deficiency.

### Task C: reciprocal flattening
Implement:
- reciprocal weight computation,
- clipping rules,
- parameter validation for `r_t`.

### Task D: exponential lifting
Implement:
- shaping function `\phi(\lambda; r_t)`,
- lift gain `\beta`,
- clipping rules,
- composition with reciprocal weights.

### Task E: retained-coordinate output
Implement:
- `c_t = U_t^\top\tilde{x}_t`,
- `z_t = W_t c_t`,
- diagnostic logging of intermediate weights.

## 4. Baselines that must be implemented
The baseline set fixed in Phase 1 should be implemented exactly:
1. raw retained spectral coordinates,
2. online PCA / low-rank covariance coordinates,
3. reciprocal flattening alone,
4. exponential lift alone.

These are required to determine whether the ordered REST composition contributes anything beyond its parts.

## 5. Synthetic experiments
The first experiments should be synthetic and tightly controlled.

### Experiment family A: drifting low-rank subspace
Goal:
- test how stable the representation is under controlled rotation or slow drift of dominant directions.

### Experiment family B: rotating anisotropic Gaussian stream
Goal:
- test whether reciprocal flattening reduces instability caused by changing anisotropy,
- test whether exponential lifting restores useful contrast.

### Experiment family C: smoothly deforming manifold toy data
Goal:
- test whether the retained-coordinate representation behaves better than raw low-rank coordinates under changing local geometry.

## 6. Metrics to record
Phase 3 should evaluate at least:
- output stability across adjacent timesteps,
- spectral-weight sensitivity,
- condition-number proxies,
- distortion proxies in the retained coordinates,
- runtime cost per update,
- parameter sensitivity with respect to `k`, `r_t`, `\beta`, and clipping.

If a simple downstream task is included, it should remain secondary to these structural diagnostics.

## 7. Testing requirements
The following tests should exist before Phase 3 is considered complete:
- covariance operator shape and PSD sanity checks,
- eigendecomposition ordering checks,
- clipping behavior checks,
- deterministic transform output checks on fixed toy inputs,
- comparison tests verifying that REST differs from each baseline in a controlled way.

## 8. Phase 3 decision questions
At the end of Phase 3, the repository should be able to answer:
1. Does REST improve stability over raw retained spectral coordinates?
2. Does the reciprocal-then-exponential ordering outperform flattening alone?
3. Does exponential lifting restore structure or mostly add sensitivity?
4. Is the covariance-based implementation numerically stable enough to justify deeper theory and broader experiments?

## 9. What Phase 3 should avoid
To keep the project disciplined, Phase 3 should avoid:
- adding graph-based variants too early,
- expanding into application datasets before synthetic behavior is understood,
- claiming empirical superiority before parameter sensitivity is measured,
- introducing learned or neural variants before the deterministic transform is stable.

## 10. Exit condition into Phase 4
Phase 3 should hand off to the next stage only if the repository has:
1. working implementation of the canonical REST transform,
2. functioning baseline implementations,
3. reproducible synthetic experiments,
4. a first empirical note documenting where REST helps and where it does not.

## Conclusion
Phase 3 is where the project must earn the right to keep going. Phase 2 made REST precise; Phase 3 must show that the precise object is computationally viable and empirically distinguishable from simpler baselines.
