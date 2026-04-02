# PHASE3_EVALUATION_NOTE

## Status
Phase 3 complete at the minimal implementation-and-synthetic-validation level.

## Scope
This note summarizes the first controlled synthetic experiments for the canonical covariance-based retained-coordinate REST formulation. The results are intentionally modest and diagnostic rather than publication-grade.

## Experiments run
- **drifting_low_rank** — dimension=6, window=24, rank=2, ridge_scale=0.5, beta=0.7, evaluated_samples=117
- **rotating_anisotropic_gaussian** — dimension=6, window=24, rank=2, ridge_scale=0.5, beta=0.7, evaluated_samples=117
- **deforming_manifold** — dimension=6, window=24, rank=2, ridge_scale=0.5, beta=0.7, evaluated_samples=117

## Core metrics

### drifting_low_rank

| Metric | Value |
| --- | ---: |
| REST adjacent-output stability | 2.774790 |
| Raw retained coordinates stability | 2.532904 |
| PCA-energy baseline stability | 3.831726 |
| Reciprocal-only stability | 1.647284 |
| Exponential-only stability | 4.400251 |
| Mean weight sensitivity | 0.025753 |
| Mean condition proxy | 1.381806 |
| Max condition proxy | 1.579274 |
| Mean runtime per update (ms) | 0.101687 |

### rotating_anisotropic_gaussian

| Metric | Value |
| --- | ---: |
| REST adjacent-output stability | 3.165214 |
| Raw retained coordinates stability | 3.847463 |
| PCA-energy baseline stability | 10.320448 |
| Reciprocal-only stability | 1.802511 |
| Exponential-only stability | 7.180127 |
| Mean weight sensitivity | 0.037252 |
| Mean condition proxy | 1.971944 |
| Max condition proxy | 2.454292 |
| Mean runtime per update (ms) | 0.097551 |

### deforming_manifold

| Metric | Value |
| --- | ---: |
| REST adjacent-output stability | 0.357142 |
| Raw retained coordinates stability | 0.264780 |
| PCA-energy baseline stability | 0.240708 |
| Reciprocal-only stability | 0.258411 |
| Exponential-only stability | 0.394564 |
| Mean weight sensitivity | 0.019769 |
| Mean condition proxy | 1.096245 |
| Max condition proxy | 1.240753 |
| Mean runtime per update (ms) | 0.096886 |

## Parameter sensitivity (beta sweep on rotating anisotropic Gaussian)

| beta | REST stability | Mean condition proxy | Mean weight sensitivity |
| ---: | ---: | ---: | ---: |
| 0.0 | 1.817353 | 2.397389 | 0.037112 |
| 0.4 | 2.507513 | 2.170911 | 0.038343 |
| 0.8 | 3.474926 | 1.967090 | 0.037316 |
| 1.2 | 4.836566 | 1.783534 | 0.034301 |

## Initial takeaways
1. REST is now implemented in the canonical retained-coordinate covariance setting and produces stable outputs under controlled synthetic drift.
2. The reciprocal-then-exponential composition is empirically distinguishable from raw, reciprocal-only, and exponential-only baselines.
3. The beta sweep shows that the exponential lift materially changes stability and conditioning behavior, so it is not a vacuous post-processing step.
4. These results are still diagnostic rather than definitive: they establish computational viability, not empirical dominance.

## Limitations
- Only synthetic streams were used.
- The covariance-based formulation is the only implemented operator family.
- The experiments do not establish superiority on downstream tasks.
- The theorem draft remains modest and local-in-time.

## Phase 3 exit judgment
Phase 3 is complete because the repository now contains a working REST implementation, functioning baseline implementations, reproducible synthetic experiments, tests, and a first empirical note documenting behavior under controlled drift.
