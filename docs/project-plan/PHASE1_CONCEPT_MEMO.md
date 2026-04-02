# PHASE1_CONCEPT_MEMO

## Purpose
This memo completes the first conceptual half of Phase 1 for the DOG/REST repository. Its job is to reduce ambiguity, narrow the current formulation, and define what the project is actually claiming at this stage.

## 1. Core problem statement
The repository is trying to solve a specific representation problem for **streaming, nonstationary data**:

> How can we maintain a numerically stable working representation for downstream computation when the data's local geometry changes over time, so that a fixed Euclidean embedding or a one-shot batch spectral method is no longer trustworthy?

In the current materials, the failure mode of standard approaches is not merely coordinate drift. The deeper issue is drift in the **effective local metric structure**:
- curvature may change,
- anisotropy may change,
- dominant directions may rotate or deform,
- neighborhood structure may evolve,
- and the resulting working coordinates may become numerically misleading.

A useful method therefore needs to do three things at once:
1. **Track changing local geometry** from a stream.
2. **Suppress unstable or distortion-dominated modes** instead of treating them as signal by default.
3. **Return a usable Euclidean working representation** for ordinary downstream computation.

This is the tightest and most defensible problem framing for DOG/REST.

## 2. Canonical DOG vs REST distinction
The repository becomes much clearer if these terms are fixed now.

### DOG
**Differential Operator Geometry (DOG)** should denote the **umbrella research program**:
- geometry is not background structure but part of the computational mechanism,
- data is modeled as living in **time-varying local spaces**,
- analysis is performed through evolving local operators rather than one fixed embedding,
- multiple future methods could eventually live under this umbrella.

DOG is therefore the **framework / thesis / research worldview**.

### REST
**REST (Reciprocal–Exponential Spectral Transforms)** should denote the **current concrete method family** inside DOG:
1. construct or update a local operator from streaming data,
2. compute a low-rank spectral decomposition,
3. apply reciprocal flattening,
4. apply exponential lifting,
5. emit the transformed Euclidean working representation.

REST is therefore the **named operator pipeline**.

### Canonical interpretation
- **DOG = framework**
- **REST = current method candidate**

This distinction prevents the project from making claims that are broader than the current evidence supports.

## 3. Minimum viable formulation choices
Phase 1 is not complete until the project chooses one concrete formulation path. The following choices are the minimum needed to reduce ambiguity.

### A. Canonical object of decomposition
Use the **windowed local operator formulation** as canonical.

Recommended default:
- define a symmetric positive semidefinite local operator `L_t`,
- build it from a sliding window of recent data,
- use **local covariance** as the Phase 1 default instantiation.

Why this should be canonical now:
- it is easier to define than a Jacobian/pullback construction,
- it is easier to compute incrementally,
- it is easier to analyze with perturbation tools,
- it gives a clean eigendecomposition,
- it aligns naturally with streaming baselines.

The Jacobian/pullback viewpoint should remain in the repository as geometric motivation or later specialization, not as a co-equal main formulation in the next draft.

### B. Canonical pipeline
Use the following single pipeline as the official REST shape for Phase 1:
1. construct `L_t`,
2. compute `L_t = U_t \Lambda_t U_t^T`,
3. retain rank `k`,
4. apply reciprocal flattening to the retained spectrum,
5. apply exponential lifting,
6. output Euclidean working coordinates.

Do **not** keep the Jacobian/SVD and operator/eigendecomposition pictures as equal main pathways in the next internal draft.

### C. Replace symbolic `e^2` with a tunable gain parameter
Adopt a parameter such as `\beta > 0` for the lift gain.

Recommended Phase 1 notation:
- `r_t` = damping / ridge scale,
- `\beta` = lift gain,
- `\phi(\lambda; r_t)` = shaping function,
- `k` = retained working rank.

The current symbolic `r^{e^2}` language is memorable, but too mnemonic to function as stable mathematical notation.

### D. Make the operator action explicit
State clearly that REST outputs a **low-dimensional Euclidean coordinate representation** obtained by reweighting the leading eigenbasis of `L_t`.

That should be the default Phase 1 interpretation of the output, rather than saying REST simultaneously acts in tangent space, ambient space, and operator-induced function space.

### E. Fix a default control policy
Even if heuristic for now, the repository should define operational defaults:
- `k`: fixed small rank or explained-variance threshold,
- `r_t`: median (or chosen quantile) of retained eigenvalues,
- `\beta`: small constant with clipping,
- transformed-eigenvalue clipping bounds.

Without this, stability remains verbal rather than executable.

### F. Narrow the first theorem target
Do not try to prove the entire DOG worldview immediately.

The first theorem target should be modest:
- a **single-step perturbation/stability bound** for the REST map,
- under bounded perturbation of `L_t`,
- with a retained spectral gap,
- and clipped lift behavior.

That is realistic, useful, and compatible with the repository's current maturity.

## 4. Immediate project claims the repository can safely make
At the end of Phase 1, the project can safely claim:
- DOG is a research program about **geometry as a computational medium** for streaming data.
- REST is a candidate operator pipeline implementing that idea.
- REST consists of an **ordered reciprocal-then-exponential spectral transform**.
- The current contribution is a **clear method architecture and research direction**, not a finished theorem set or validated benchmark result.

The repository should **not yet** claim:
- fully proved near-isometry,
- general angle preservation across repeated updates,
- superiority over all standard streaming baselines,
- or that DOG is already a mature new field.

## 5. 5–10 page internal idea-paper outline
The next internal paper-like document should follow this structure.

### Title
**Differential Operator Geometry for Streaming Data: A Reciprocal–Exponential Spectral Preconditioner**

### 1. Introduction
Explain why fixed-geometry assumptions fail under streaming geometric drift. Introduce DOG as the broader research idea and REST as the first concrete method candidate.

### 2. Problem setting and motivation
Define the streaming setting and why a stable Euclidean working representation is needed when local geometry changes over time.

### 3. DOG framework
Describe the architectural thesis:
- evolving local spaces,
- operator-mediated computation,
- geometry as mechanism rather than backdrop.

Keep this section conceptual and short.

### 4. REST formulation
This is the technical core:
- define the stream,
- define `L_t`,
- define eigendecomposition,
- define reciprocal flattening,
- define exponential lifting,
- define output representation,
- define `k`, `r_t`, `\beta`, and clipping.

### 5. Interpretive rationale
Explain why the ordered composition matters:
- reciprocal flattening as spectral de-biasing / geometric preconditioning,
- exponential lifting as controlled structure restoration,
- the ordered composition as the novelty candidate.

### 6. First theoretical properties
State only what can actually be proved in Phase 2:
- boundedness,
- perturbation stability,
- perhaps a modest distortion statement in the retained subspace.

### 7. Minimal algorithm and complexity
Provide one clear algorithm box and cautious complexity discussion.

### 8. Evaluation plan
Focus on synthetic streaming tests:
- drifting low-rank subspaces,
- rotating anisotropic Gaussian streams,
- smoothly deforming manifold toy problems.

Compare first against online PCA and simple spectral baselines.

### 9. Limitations and open questions
Explicitly acknowledge:
- dependence on operator choice,
- unresolved repeated-update theory,
- parameter sensitivity,
- and lack of empirical validation so far.

### 10. Conclusion
Restate the narrow contribution: DOG is the umbrella program; REST is the first formal operator candidate inside it.

## 6. Concrete decision points for the next 2–4 weeks

### Week 1
Lock down:
1. DOG vs REST naming policy,
2. canonical local operator,
3. canonical output representation,
4. canonical parameters and clipping rules.

### Week 1–2
Write a short internal theory note containing:
- symbol table,
- exact REST definition,
- assumptions,
- one theorem target,
- one algorithm box.

### Week 2
Complete one theorem fully:
- best candidate: a single-step perturbation/stability bound under bounded perturbation of `L_t`.

### Week 2–3
Build the smallest useful benchmark harness:
- synthetic streaming generators,
- `L_t` updates,
- low-rank eigendecomposition,
- REST transform,
- baseline comparators.

### Week 3–4
Use experiments to answer four direct questions:
1. Does REST improve stability over raw spectral coordinates?
2. Does it preserve useful structure better than flattening alone?
3. Does exponential lifting help, or merely add sensitivity?
4. How fragile is behavior with respect to `\beta`, `r_t`, rank, and clipping?

## 7. Bottom-line Phase 1 judgment
The strongest path forward is:
- narrow DOG conceptually,
- formalize REST concretely,
- pick one canonical operator,
- prove one real result,
- test one controlled benchmark family.

The repository should avoid a manifesto-style posture until REST has at least:
1. one finished proof,
2. one clean synthetic benchmark result.

That is the shortest path from intriguing concept to credible research artifact.
