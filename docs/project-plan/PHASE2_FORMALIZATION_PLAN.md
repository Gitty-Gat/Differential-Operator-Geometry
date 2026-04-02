# PHASE2_FORMALIZATION_PLAN

## Purpose
Phase 2 converts the Phase 1 concept work into a mathematically precise method specification. The goal is not to prove everything at once. The goal is to produce one canonical formalism, one consistent notation system, and one complete initial theorem.

## Phase 2 objective
At the end of Phase 2, the repository should contain:
1. one canonical REST definition using a single operator formulation,
2. one consistent symbol table,
3. one clearly stated assumption set,
4. one complete single-step perturbation/stability theorem,
5. one algorithm box aligned with the formal notation.

## 1. Canonical mathematical setting
The canonical setting for Phase 2 is:
- streaming observations `x_t \in \mathbb{R}^d`,
- sliding-window covariance-based operator `L_t`,
- retained low-rank eigendecomposition `L_t = U_t \Lambda_t U_t^T`,
- output coordinates in the retained basis.

### Why this is the canonical setting
- simplest to define,
- simplest to benchmark,
- simplest to compare to online PCA and whitening,
- easiest to analyze with standard perturbation methods.

Graph, Fisher, and Jacobian formulations should be deferred until the covariance case is internally coherent.

## 2. Formal notation work
Phase 2 should standardize the following notation immediately.

### Objects
- `x_t` = streaming observation
- `\mu_t` = windowed mean
- `\tilde{x}_t = x_t - \mu_t` = centered observation
- `L_t` = local PSD operator
- `U_t` = retained eigenbasis
- `\Lambda_t = diag(\lambda_{t,1}, \dots, \lambda_{t,k})` = retained eigenvalues
- `k` = retained rank
- `r_t` = reciprocal damping scale
- `\beta` = exponential lift gain
- `\phi(\lambda; r_t)` = shaping function for lift
- `z_t` = REST output coordinates

### Transform notation
Use a two-stage diagonal transform in the retained basis:
- reciprocal spectral weights,
- exponential lift weights,
- composite retained-coordinate transform.

The symbolic `r^{e^2}` notation should remain only in archived source material, not in future formal sections.

## 3. Formal REST definition to be completed
Phase 2 should define the transform explicitly in the retained basis.

A clean target structure is:
1. compute retained coordinates `c_t = U_t^T \tilde{x}_t`,
2. apply reciprocal weights `D_inv(\Lambda_t, r_t)`,
3. apply exponential weights `D_exp(\Lambda_t, r_t, \beta)`,
4. define
   `z_t = D_exp D_inv c_t`.

If needed, the ambient reconstruction can be defined separately, but the coordinate-space version should be primary.

## 4. Assumption set for the first theorem
Phase 2 should adopt a modest assumption set targeted to one theorem.

### Recommended assumptions
1. **PSD operator assumption**: `L_t` is symmetric positive semidefinite.
2. **Retained spectral gap**: `\lambda_{t,k} - \lambda_{t,k+1} \ge \gamma > 0` when the `(k+1)`st eigenvalue is defined.
3. **Bounded perturbation/drift**: `||L_t - L_{t-1}||_2 \le \delta`.
4. **Bounded transformed weights**: reciprocal and exponential weights are clipped or otherwise bounded.
5. **Nondegenerate retained coordinates** where needed for distortion statements.

These assumptions should be stated cleanly before any theorem claims.

## 5. First theorem target
The first theorem should be intentionally modest.

### Target theorem
A **single-step perturbation/stability theorem** showing that under bounded perturbation of `L_t`, retained spectral gap, and clipped weights, the REST transform changes in a controlled way.

Possible theorem forms:
- operator norm bound on the change in the retained transform,
- coordinate distortion bound in the retained basis,
- condition-number bound for the composite diagonal transform.

### Why this is the right first theorem
- tractable,
- directly relevant to streaming updates,
- enough to support later experiments,
- avoids overcommitting to long-horizon repeated-update theory too early.

## 6. Proof dependencies
The proof strategy will likely rely on standard perturbation tools such as:
- eigenspace perturbation bounds,
- spectral gap control,
- boundedness of diagonal transform functions,
- norm inequalities for composed transforms.

The repository does not need to prove every perturbation lemma from scratch; it needs to use them carefully and state assumptions explicitly.

## 7. Algorithm box requirements
By the end of Phase 2, the repository should include one algorithm description matching the formal notation exactly.

### It must define
- how `L_t` is updated,
- how the retained eigensystem is extracted,
- how `r_t` is chosen,
- how clipping is applied,
- how `z_t` is emitted.

This algorithm description should avoid symbolic inconsistency and should match the theorem setting as closely as possible.

## 8. Phase 2 deliverables
Phase 2 is complete when the repository contains:
- `REST_METHOD_NOTE.md` or equivalent,
- a symbol table,
- a formal transform definition,
- a first theorem and proof draft,
- an algorithm box aligned with the theory,
- a short note describing how this formalization differs from Phase 1 conceptual material.

## 9. What Phase 2 should explicitly avoid
To keep the work credible and finishable, Phase 2 should avoid:
- claiming repeated-update near-isometry without proof,
- switching between covariance and graph operators mid-proof,
- keeping Jacobian/SVD and operator/eigendecomposition as equal primary formalisms,
- adding application-driven claims before the theorem is stable,
- expanding DOG philosophically faster than REST is formalized.

## 10. Exit condition into Phase 3
Phase 2 should hand off to implementation only once the repository can answer yes to all of these:
1. Is there one canonical formal definition of REST?
2. Is the notation consistent across all active documents?
3. Is there one theorem that is fully stated and fully proved?
4. Is the algorithm box faithful to the theorem setting?

If the answer is no to any of these, Phase 2 is not done.

## Conclusion
Phase 2 should be treated as the discipline phase of the project. Its success is not measured by breadth, but by precision: one operator setting, one notation system, one theorem, one algorithm. If that is completed well, the repository will have moved from an intriguing concept archive to a genuine early-stage mathematical method.
