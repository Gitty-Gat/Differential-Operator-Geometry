# PHASE5_NONCOMMUTING_VARIANT_SPIKE

## Purpose
This note scopes a minimal, high-leverage spike to test whether a non-commuting variant of REST can restore a genuinely distinguishable ordering effect.

## Why this spike exists
Phase 4 established that in the current retained-coordinate diagonal formulation:
- reciprocal and exponential maps commute,
- the reversed-order ablation is algebraically identical,
- so ordering cannot currently serve as a distinct empirical source of novelty.

A short spike is justified only if it can answer whether this is a removable architectural artifact or an inherent limitation of the current formulation family.

## Minimal acceptable spike criteria
A candidate non-commuting variant must:
1. remain interpretable,
2. remain computationally lightweight enough for the existing experimental framework,
3. produce a genuinely distinguishable ordering effect,
4. not destroy the stability profile so completely that the method loses practical value.

## Candidate directions

### Option 1: Off-diagonal coupling between stages
Insert a simple coupling matrix `M_t` between reciprocal and exponential weighting so that
- reciprocal weights act in one retained basis,
- a coupling map mixes coordinates,
- exponential weights act after mixing.

This is the most direct way to break commutativity while staying close to the current architecture.

### Option 2: Two-basis formulation
Allow the flattening and lifting stages to use different bases derived from related but non-identical local operators.

This is mathematically more interesting but also more invasive.

### Option 3: Graph-Laplacian local operator variant
Test whether moving away from the covariance-only retained basis naturally produces a richer operator interaction.

This is higher effort and should only be attempted if the simpler spike directions fail or are unconvincing.

## Evaluation rule for the spike
The spike should be declared successful only if all of the following occur:
1. the reversed-order ablation becomes empirically distinguishable,
2. the new variant remains numerically stable on at least the primary synthetic families,
3. the additional complexity appears justified by the new behavior.

If not, the project should stop treating ordering as a central novelty claim and continue with the preconditioner framing instead.

## Recommended scope limit
Do **not** turn this into a full architecture branch yet. Keep the spike limited to:
- one implementation path,
- one or two synthetic families,
- one focused comparison against the current canonical formulation.

## Exit question
At the end of the spike, the project should be able to answer:

> Is a non-commuting REST variant promising enough to justify architectural investment, or should the repository continue under the simpler geometric-preconditioner framing?
