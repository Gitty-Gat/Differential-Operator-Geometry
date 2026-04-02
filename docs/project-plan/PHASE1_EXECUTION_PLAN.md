# PHASE1_EXECUTION_PLAN

## Purpose
This plan turns the conceptual and literature outputs of Phase 1 into a concrete execution sequence. It is intentionally narrow: the goal is to create one coherent research track, not to explore every future branch at once.

## Phase 1 completion criteria
Phase 1 is complete when all of the following are true:
1. DOG vs REST terminology is fixed.
2. One canonical operator formulation is selected.
3. One canonical notation system is selected.
4. One internal idea-paper draft exists.
5. One literature-positioning memo exists.
6. One explicit set of short-term decision points exists.

These criteria are now satisfied by the files in `docs/project-plan/`.

## Immediate follow-on work sequence
Although Phase 1 is now complete at the documentation level, the work below defines the handoff into Phase 2 and protects against concept drift.

### Step 1. Freeze the canonical formulation
Use the following as the official working setup:
- DOG = umbrella framework
- REST = concrete method family
- `L_t` = windowed covariance-based PSD operator
- retained eigendecomposition = canonical spectral object
- output = Euclidean coordinates in retained basis
- parameters = `k`, `r_t`, `\beta`, clipping bounds

### Step 2. Convert the formulation into a method note
The next internal theory note must include:
- symbol table,
- formal REST transform definition,
- assumptions,
- one theorem target,
- one algorithm box.

This note should become the internal reference for Phase 2 proofs and Phase 3 implementation.

### Step 3. Define baseline comparisons before implementation expands
The first baseline set is fixed as:
1. raw retained spectral coordinates,
2. online PCA / low-rank covariance coordinates,
3. reciprocal flattening alone,
4. exponential lift alone.

This prevents later experiments from being tuned without a stable comparison set.

## Four-week handoff schedule

### Week 1
**Goal:** finish formal narrowing

Tasks:
- convert Phase 1 decisions into formal notation,
- define exact transform equations,
- define clipping rules,
- define the retained coordinate output,
- define the theorem target precisely.

Deliverables:
- Phase 2 formalization plan,
- internal method note skeleton.

### Week 2
**Goal:** one completed theorem target

Tasks:
- state single-step perturbation/stability result,
- fix assumptions on perturbation size and retained spectral gap,
- prove one complete bound,
- identify where clipping enters the proof.

Deliverables:
- first complete proof draft,
- theorem statement aligned with notation.

### Week 3
**Goal:** minimal synthetic implementation harness

Tasks:
- implement streaming covariance updates,
- implement retained eigendecomposition,
- implement reciprocal flattening,
- implement exponential lifting,
- implement baseline transforms,
- add diagnostic logging for spectral drift and transformed weights.

Deliverables:
- prototype code structure,
- first synthetic stream generators.

### Week 4
**Goal:** empirical sanity check

Tasks:
- run drifting low-rank stream tests,
- run rotating anisotropic Gaussian tests,
- compare REST vs baselines,
- measure stability, distortion proxies, and sensitivity to parameters.

Deliverables:
- first empirical note,
- go/no-go assessment for continued REST development.

## Questions that must be answerable at the end of the handoff
By the end of this sequence, the project should be able to answer:
1. Is the covariance-based REST formulation mathematically coherent?
2. Does reciprocal-then-exponential ordering give a measurable benefit over simpler alternatives?
3. Does the exponential lift restore structure or mainly introduce sensitivity?
4. Is there one proof and one empirical result strong enough to justify a draft paper?

## Risk controls
To prevent the project from drifting back into abstraction, the following rules should hold:
- do not expand the operator family until the covariance-based case is understood,
- do not claim repeated-update near-isometry before single-step stability is proved,
- do not bring in graph or Jacobian variants until the baseline covariance case is benchmarked,
- do not widen DOG as a manifesto until REST has one theorem and one experimental result.

## Output of Phase 1
Phase 1 has now produced:
- a concept memo,
- a literature-positioning memo,
- canonical formulation decisions,
- an internal idea-paper draft,
- and this execution plan.

That is enough structure to begin formal mathematical work in Phase 2 without ambiguity about what is being formalized.
