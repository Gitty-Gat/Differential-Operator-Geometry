# PHASE1_DECISIONS

## Purpose
This file records the canonical project choices adopted at the end of Phase 1 so that future theory, implementation, and evaluation work use the same base formulation.

## Status
**Adopted for Phase 1 and Phase 2 planning**

These decisions are intentionally narrow. They are not claims about the only valid long-term form of DOG/REST; they are the minimum choices required to stop conceptual drift and enable rigorous progress.

## 1. DOG vs REST naming policy

### DOG
**Differential Operator Geometry (DOG)** is the umbrella research framework.

DOG means:
- evolving local geometry is part of the computational mechanism,
- data is treated as living in time-varying local spaces,
- operator evolution mediates analysis,
- multiple future methods may belong under this umbrella.

### REST
**Reciprocal–Exponential Spectral Transforms (REST)** is the concrete method family currently being formalized and tested.

REST means:
- define a local operator from streaming data,
- compute a low-rank spectral representation,
- apply reciprocal flattening,
- apply exponential lifting,
- emit a Euclidean working representation.

### Policy
Future repository documents should avoid using DOG and REST interchangeably.

## 2. Canonical local operator for the next stage
The canonical Phase 1 / Phase 2 operator is:

> a **windowed covariance-based symmetric positive semidefinite operator** `L_t`

### Rationale
- easiest to define clearly,
- easiest to implement in streaming form,
- easiest to compare to online PCA and whitening baselines,
- easiest to analyze using perturbation methods,
- avoids premature complexity from graph updates or Jacobian estimation.

### Status of alternatives
The following remain valid future branches, but not the canonical immediate path:
- graph Laplacian operators,
- Fisher information operators,
- Jacobian / pullback formulations.

## 3. Canonical decomposition
The official immediate formulation is:

`L_t = U_t \Lambda_t U_t^T`

with:
- retained working rank `k`,
- retained eigenvalues `\lambda_{t,1}, \dots, \lambda_{t,k}`,
- retained basis `U_t`.

The Jacobian/SVD formulation remains geometric motivation, not the canonical computational definition for the next phase.

## 4. Canonical output representation
REST should be treated as outputting:

> a **low-dimensional Euclidean coordinate representation** in the retained spectral basis.

Concretely, the default output is a coordinate vector `z_t` or equivalent reweighted low-rank representation rather than an abstract unspecified working space.

## 5. Canonical parameterization
The repository adopts the following Phase 1 notation:
- `k` = working rank,
- `r_t` = reciprocal damping / ridge scale,
- `\beta` = exponential lift gain,
- `\phi(\lambda; r_t)` = smooth shaping function used in the lift,
- clipping bounds on transformed spectral weights.

### Important notation decision
The symbolic shorthand `r^{e^2}` is no longer the canonical mathematical form.

It may still appear historically or motivationally in source-material archives, but future formal documents should use `\beta` and an explicit transform definition.

## 6. Canonical transform order
The ordered composition adopted for REST is:
1. **reciprocal flattening first**,
2. **exponential lifting second**.

This ordering is treated as the main novelty candidate and should be preserved in upcoming theory and experiments unless empirical evidence strongly contradicts it.

## 7. Phase 2 theorem target
The first rigorous theorem target is intentionally narrow:

> a **single-step perturbation/stability bound** for the REST transform under bounded perturbation of `L_t`, assuming a retained spectral gap and clipped spectral weights.

### Why this is the target
- it is realistic,
- it is mathematically useful,
- it gives a publishable proof target sooner than broad repeated-update claims,
- it supports later empirical benchmarking.

## 8. Initial baseline comparison set
The next stage should compare REST against the following immediate baselines:
1. online PCA / low-rank covariance coordinates,
2. whitening or inverse-spectral flattening alone,
3. exponential lift alone,
4. raw retained spectral coordinates without REST reweighting.

Dynamic graph-based or heavier geometric baselines can be added later if the canonical operator expands beyond covariance.

## 9. Immediate evaluation questions
The project should now be organized to answer these questions:
1. Does REST improve stability over raw low-rank spectral coordinates?
2. Does the reciprocal-then-exponential ordering outperform flattening alone?
3. Does the exponential lift restore useful structure rather than merely amplify sensitivity?
4. How sensitive is behavior to `k`, `r_t`, `\beta`, and clipping?

## 10. Decision discipline for future edits
Any proposal to change one of the canonical choices above should specify:
- what ambiguity or failure it resolves,
- what theorem or experiment requires the change,
- what new baselines the change would force,
- and whether the project remains clearly distinguishable from online PCA, whitening, or dynamic spectral embedding baselines.

## Conclusion
Phase 1 is complete only if the project stops drifting between multiple identities and formulations. These decisions establish one narrow, coherent track:
- DOG as umbrella framework,
- REST as current method family,
- covariance-based `L_t` as canonical immediate operator,
- reciprocal-then-exponential composition as the core transform,
- and single-step stability as the first theorem target.
