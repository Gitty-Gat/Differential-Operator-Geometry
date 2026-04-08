# PRECONDITIONER POSITIONING NOTE

_Last updated: 2026-04-08_

## Current honest framing
The strongest current contribution in this repo is **not** a general proof that stage ordering creates a distinct computational mechanism. The strongest current contribution is narrower:

> REST is a covariance-based streaming geometric preconditioner in retained spectral coordinates, with a partial one-step stability story and controlled synthetic support.

## What this means
- The repo studies a concrete operator family rather than a universal geometry-computation thesis.
- The implemented covariance path is the main line, not a placeholder.
- Reciprocal and exponential weighting should currently be understood as commuting diagonal reweightings in the retained-coordinate setting.
- The practical question is whether that preconditioning view gives useful behavior in some regimes, not whether it wins everywhere.

## What should not be claimed right now
- That ordering-sensitive novelty is independently established in the active architecture.
- That the current theorem draft proves broad geometric superiority.
- That synthetic results already justify broad real-world performance claims.

## Consequence for execution
The next good slices are:
1. sharpen method and theorem text so they match this framing,
2. run one narrow validation where preconditioning might matter,
3. keep the repo control layer simple and honest.
