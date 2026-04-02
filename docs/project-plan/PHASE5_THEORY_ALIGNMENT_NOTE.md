# PHASE5_THEORY_ALIGNMENT_NOTE

## Purpose
This note completes the main theory-alignment task of Phase 5. Its goal is to make the theorem language match the method that is actually implemented and evaluated in the repository.

## Strongest honest framing
In the current repository state, REST is best described as:

> a **streaming geometric preconditioner** in retained spectral coordinates.

This is stronger and more accurate than framing the current implementation as an already-established ordering-sensitive mechanism.

## Why the reframing is necessary
Phase 4 established the following:
1. the current implementation is computationally viable,
2. it is empirically distinguishable from several simple baselines,
3. but in the retained-coordinate diagonal formulation the reciprocal and exponential weighting maps commute,
4. so reversed-order ablations are algebraically identical to the canonical order.

That means the theorem should not imply that the current implementation already exhibits a distinct non-commuting ordering effect.

## What the theorem should support
The strongest current theorem target is:

> a **single-step perturbation/stability bound for the retained-coordinate geometric preconditioner** induced by the covariance-based REST transform.

This framing is well aligned with what the repository currently has:
- covariance PSD local operator,
- retained eigendecomposition,
- bounded spectral weight maps,
- one-step drift diagnostics,
- monitored spectral-gap behavior.

## What the theorem should not currently support
The theorem should **not** currently be framed as proving:
- a unique reciprocal-then-exponential ordering effect,
- a non-commuting transform mechanism,
- long-horizon near-isometry,
- angle preservation under repeated updates,
- or broad empirical superiority.

## Assumption-to-implementation alignment
The theorem remains strongest when interpreted through the implementation controls already present in the repository:

| Theorem component | Implementation anchor |
| --- | --- |
| PSD operator | sliding-window covariance construction |
| bounded drift | synthetic stream design + drift diagnostics |
| retained spectral gap | logged gap diagnostics |
| bounded transform laws | bounded reciprocal/exponential maps with clipping available |
| retained-coordinate output | `z_t = W_t U_t^\top \tilde{x}_t` in code |

## Revised interpretation of the composite transform
In the current architecture, the composite transform should be interpreted as:
- a diagonal retained-coordinate reweighting,
- intended to improve conditioning and representation stability,
- rather than as direct evidence that stage ordering is independently meaningful.

This is exactly why the phrase **geometric preconditioner** is the right current description.

## Theory-tightening tasks still remaining
Phase 5 does not finish the proof, but it does define the next tightening tasks clearly:
1. make the theorem title and surrounding prose consistently preconditioner-focused,
2. sharpen where constants depend on spectral gap and weight bounds,
3. explicitly connect theorem assumptions to the diagnostics logged in Phase 4,
4. keep any ordering-based novelty claims out of the theorem until a non-commuting variant exists.

## Alignment conclusion
The repository is in a stronger position when it claims exactly this:

> The current covariance-based REST implementation defines a retained-coordinate geometric preconditioner with a plausible and partially formalized one-step stability theory.

That claim is honest, supported, and compatible with the empirical evidence now present in the repo.
