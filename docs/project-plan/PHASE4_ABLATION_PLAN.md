# PHASE4_ABLATION_PLAN

## Purpose
This document records the ablation matrix Phase 4 is required to execute. The goal is to isolate which parts of the current covariance-based retained-coordinate REST formulation actually matter.

## Required ablation families

### 1. Representation-order ablations
- raw retained coordinates
- reciprocal-only
- exponential-only
- reciprocal-then-exponential (canonical REST)
- exponential-then-reciprocal

## Key question
Does the ordered composition matter in the current implementation, or are the diagonal maps effectively commuting in the retained-coordinate basis?

### 2. Functional-form ablations
- reciprocal exponent `-1/2` versus alternative reciprocal exponents
- default shaping function `phi(\lambda; r)` versus alternatives
- fixed ridge scale versus adaptive ridge scale
- conservative versus aggressive clipping bounds

## Key question
Are the current transform laws doing real work, or are they one arbitrary choice among many equivalent ones?

### 3. Parameter ablations
- beta sweep
- ridge-scale sweep
- window-size sweep
- retained-rank sweep
- clipping-range sweep

## Key question
Under what parameter regimes is REST stable, useful, fragile, or unnecessary?

### 4. Failure-mode ablations
- sparse high-noise stream
- collapsing spectral-gap regimes
- over-large beta
- too-small ridge scale

## Key question
Where does REST fail, and does it fail for understandable reasons that align with the theorem draft?

## Output requirements
The Phase 4 ablation work must produce:
- quantitative tables,
- diagnostic plots,
- a clear statement of which ablations meaningfully change behavior,
- and a recommendation on whether the current formulation should continue unchanged, be refined, or be narrowed.
