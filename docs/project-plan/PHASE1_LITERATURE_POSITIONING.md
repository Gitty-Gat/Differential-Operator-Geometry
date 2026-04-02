# PHASE1_LITERATURE_POSITIONING

## Purpose
This memo completes the literature-positioning half of Phase 1. It does not pretend to be an exhaustive external bibliography. Instead, it identifies the bodies of work DOG/REST must engage, the main overlap risks, the most defensible novelty wedges, and the search directions needed for a deeper formal literature review.

## 1. Thematic buckets of prior work DOG/REST must engage

### A. Manifold learning and spectral geometry
This is the most immediate neighborhood. DOG/REST explicitly builds local spectral descriptions of geometry and aims to produce a Euclidean working representation while respecting local structure.

Representative families:
- Laplacian Eigenmaps
- Diffusion Maps
- Isomap
- Locally Linear Embedding
- Hessian Eigenmaps / local spectral manifold methods
- graph Laplacian and spectral clustering embedding literature

Why this matters:
- These methods establish the baseline idea that local geometry and spectra can produce low-dimensional coordinates.
- DOG/REST must explain what changes when geometry is evolving and the operator is repeatedly updated online.

### B. Streaming / online subspace tracking and low-rank adaptation
REST is framed as a streaming operator pipeline. That places it directly in conversation with:
- Oja's rule and online PCA,
- incremental PCA,
- incremental SVD / eigendecomposition,
- subspace tracking methods,
- matrix sketching and streaming low-rank approximation.

Why this matters:
- These are the natural baselines for "stable low-rank working representation under streaming updates."
- DOG/REST must show that geometry-awareness contributes something beyond online variance tracking.

### C. Time-varying graphs, dynamic spectral embeddings, and temporal manifold methods
Because DOG/REST updates geometry over time rather than once in batch, it overlaps with:
- dynamic graph embedding methods,
- incremental graph Laplacian eigen-updating,
- temporal diffusion / evolving graph signal processing,
- streaming spectral clustering,
- time-dependent manifold approximation and adaptive neighborhood graph methods.

Why this matters:
- These methods already address changing relational structure and evolving spectra.
- They are close operational competitors if REST is implemented via local graph or neighborhood operators.

### D. Metric learning, whitening/preconditioning, and anisotropy correction
The reciprocal flattening step strongly overlaps with:
- PCA whitening / ZCA whitening,
- Mahalanobis normalization and metric learning,
- Fisher-information-based reweighting,
- natural-gradient-style preconditioning,
- spectral preconditioners and inverse-covariance normalization.

Why this matters:
- Reciprocal flattening may look like structured whitening or preconditioning.
- If that is all it is, the novelty claim weakens substantially.

### E. Riemannian / conformal geometry and geometry-aware representation transforms
The exponential lift and angle-preservation ambitions place DOG/REST near:
- conformal mapping and quasi-conformal distortion control,
- metric flattening and local chart linearization,
- tangent-space methods in manifold learning,
- pullback metrics and Jacobian-based local geometry analysis,
- information geometry and local metric deformation.

Why this matters:
- DOG/REST uses language about preserving angles, controlling distortion, and moving between curved local structure and Euclidean workspaces.
- Reviewers will expect a coherent connection to this literature.

### F. Operator-theoretic dynamical systems viewpoints
The repository already gestures toward operator flow, evolving local operators, and geometry as computation. That invites comparison with:
- Koopman operator methods,
- Dynamic Mode Decomposition (and streaming variants),
- transfer-operator viewpoints,
- semigroup-inspired formulations of nonstationary systems.

Why this matters:
- DOG/REST must clarify whether it is an operator-learning method, a representation method, or a geometric preconditioner.

### G. Geometric deep learning and adaptive latent geometry
Even if DOG/REST is not a neural method, the broader literature now includes:
- geometry-aware graph neural networks,
- dynamic graph neural networks,
- adaptive manifold representation learning,
- latent flow models with learned geometry,
- self-supervised geometry-sensitive embeddings.

Why this matters:
- DOG/REST should position itself as deterministic, streaming, interpretable, and low-rank rather than trying to compete on the same terms.

## 2. Specific overlap risks

### Risk 1: REST looks like online PCA plus nonlinear rescaling
If the local operator is covariance-like and the transform is merely inverse spectral damping followed by monotone reweighting, reviewers may see it as online PCA/whitening with a custom post-processing step.

### Risk 2: REST collapses into dynamic Laplacian embedding
If the canonical operator becomes a local graph Laplacian, the method could be interpreted as a streaming spectral embedding with modified eigenvalue scaling rather than a genuinely new framework.

### Risk 3: "Geometry as computation" sounds philosophical rather than technical
The DOG umbrella language is interesting, but without a precise formal statement of what is computationally new, it risks sounding rhetorical.

### Risk 4: The reciprocal step overlaps heavily with whitening/preconditioning
Flattening anisotropy via inverse spectral weights is a familiar move. Without a theorem showing that the ordered reciprocal-then-exponential composition has special properties, the flattening step alone will not look novel.

### Risk 5: The exponential lift may look like a generic spectral filter
Many operator methods apply exponential, polynomial, or diffusion-like spectral filters. If the lift is not tightly motivated, it may appear generic.

### Risk 6: Dynamic operator language overlaps with Koopman/DMD framing
If DOG/REST talks about evolving operators and streaming dynamics without clearly distinguishing the object being modeled, readers may conclude the conceptual territory is already occupied.

### Risk 7: Angle-preservation and near-isometry claims are high-risk
These claims are common and scrutinized. Without precise assumptions and proofs, they will be treated as aspirational rather than established.

## 3. Plausible novelty wedges

### Wedge A: The ordered two-stage composition
The strongest novelty candidate is not streaming geometry by itself, nor spectral filtering by itself, but the specific ordered composition:
1. reciprocal flattening to suppress distortion-dominated modes,
2. exponential lifting to restore controlled usable structure.

If this ordering can be shown to yield better conditioning-distortion tradeoffs than:
- flattening alone,
- lifting alone,
- standard whitening,
- or generic spectral filtering,
then that is a meaningful contribution.

### Wedge B: Streaming geometric preconditioner rather than general embedding method
A strong positioning move is to frame REST as a **streaming geometric preconditioner** that outputs a stable Euclidean workspace for downstream tasks, rather than as a universal competitor to all embedding methods.

This narrows the claim and makes comparisons more defensible.

### Wedge C: Explicit treatment of evolving local geometry
If the theory focuses on operator drift and changing neighborhood or metric structure, DOG/REST can distinguish itself from methods that assume fixed geometry or only weakly adapt over time.

### Wedge D: Interpretable distortion control tied to spectral quantities
A useful novelty angle would be deterministic control tied to:
- condition numbers,
- spectral gaps,
- bounded operator drift,
- clipping rules.

That matters if the project wants to be a mathematically legible alternative to heavier learned methods.

### Wedge E: Unified Jacobian/operator formulation
If the repository can rigorously connect the Jacobian/SVD view and the local-operator/eigendecomposition view, that would convert a current weakness into a substantive contribution.

### Wedge F: Stability under repeated local updates
A theorem about repeated application of the composite transform under bounded operator drift may be more publishable than broad conceptual claims about geometry as computation.

### Wedge G: Lightweight alternative to dynamic geometric learning
If experiments eventually show that REST captures enough evolving geometry to improve downstream stability or anomaly sensitivity at much lower complexity than dynamic graph or neural methods, that is a practical novelty wedge.

## 4. Recommended positioning statement
The strongest current positioning is:

> DOG is the broader research program. REST is a streaming geometric preconditioner built from an ordered reciprocal-then-exponential spectral transform.

This framing avoids two failure modes:
- overselling DOG as a new field before there is evidence,
- underselling REST as nothing more than renamed whitening.

## 5. Prioritized search directions for the next external review pass
The following query families should be used in the next literature sweep.

### Tier 1: closest technical neighbors
1. `streaming manifold learning local geometry spectral methods`
2. `online Laplacian eigenmaps dynamic graph embedding`
3. `incremental spectral embedding evolving graph Laplacian`
4. `online PCA whitening anisotropy correction streaming`
5. `subspace tracking geometry-aware representation`
6. `time-varying manifold online embedding`
7. `dynamic diffusion maps streaming data`

### Tier 2: preconditioning and metric overlap
8. `spectral preconditioning local covariance streaming`
9. `Mahalanobis metric learning online local geometry`
10. `adaptive whitening nonstationary data`
11. `information geometry streaming representation`
12. `local operator drift perturbation eigenspaces`

### Tier 3: operator and temporal geometry framing
13. `Koopman operator streaming representation geometry`
14. `online dynamic mode decomposition spectral drift`
15. `time-varying graph signal processing embedding`
16. `nonstationary spectral methods manifold drift`

### Tier 4: curvature and geometric-flow adjacency
17. `discrete Ricci flow machine learning graphs`
18. `curvature-aware graph learning streaming`
19. `Ricci flow dynamic embeddings`
20. `curvature regularization nonstationary graph learning`

## 6. Phase 1 literature takeaway
The repository should not yet claim that DOG/REST sits outside all existing traditions. The more defensible claim is narrower and stronger:
- DOG/REST lives at the intersection of manifold learning, spectral methods, streaming low-rank adaptation, and operator-based dynamic representation.
- The best current novelty candidate is the **ordered reciprocal-then-exponential composition**, especially if it can be shown to act as a useful **streaming geometric preconditioner** under evolving local geometry.

That is the literature-grounded stance the next drafts should adopt.
