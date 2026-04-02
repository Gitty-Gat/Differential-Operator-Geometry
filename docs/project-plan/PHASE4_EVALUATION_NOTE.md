# PHASE4_EVALUATION_NOTE

## Status
Phase 4 complete at the stronger evaluation-and-refinement level.

## Scope
This note expands Phase 3 by adding richer diagnostics, explicit ordering ablations, a failure-mode probe, controlled downstream tasks, quantitative success thresholds, and a go/refine/pivot decision rubric.

## Experiment families
- **drifting_low_rank** — dimension=6, window=24, rank=2, ridge_scale=0.5, beta=0.7, evaluated_samples=157
- **rotating_anisotropic_gaussian** — dimension=6, window=24, rank=2, ridge_scale=0.5, beta=0.7, evaluated_samples=157
- **deforming_manifold** — dimension=6, window=24, rank=2, ridge_scale=0.5, beta=0.7, evaluated_samples=157
- **sparse_high_noise_failure_probe** — dimension=10, window=24, rank=2, ridge_scale=0.5, beta=0.7, evaluated_samples=157

## Core ablation metrics

### drifting_low_rank

| Metric | Value |
| --- | ---: |
| REST stability | 2.920838 |
| Raw retained stability | 2.732743 |
| Reciprocal-only stability | 1.709088 |
| Exponential-only stability | 4.795530 |
| Exponential-then-reciprocal stability | 2.920838 |
| Mean condition proxy | 1.353453 |
| Min spectral gap | 0.205677 |
| Mean basis motion | 0.007023 |
| Reciprocal clip rate | 0.000000 |
| Exponential clip rate | 0.000000 |

### rotating_anisotropic_gaussian

| Metric | Value |
| --- | ---: |
| REST stability | 3.236507 |
| Raw retained stability | 3.908122 |
| Reciprocal-only stability | 1.838815 |
| Exponential-only stability | 7.290433 |
| Exponential-then-reciprocal stability | 3.236507 |
| Mean condition proxy | 1.960930 |
| Min spectral gap | 0.405271 |
| Mean basis motion | 0.003127 |
| Reciprocal clip rate | 0.000000 |
| Exponential clip rate | 0.000000 |

### deforming_manifold

| Metric | Value |
| --- | ---: |
| REST stability | 0.235760 |
| Raw retained stability | 0.169946 |
| Reciprocal-only stability | 0.181411 |
| Exponential-only stability | 0.235368 |
| Exponential-then-reciprocal stability | 0.235760 |
| Mean condition proxy | 1.038008 |
| Min spectral gap | 0.000657 |
| Mean basis motion | 0.089739 |
| Reciprocal clip rate | 0.000000 |
| Exponential clip rate | 0.000000 |

### sparse_high_noise_failure_probe

| Metric | Value |
| --- | ---: |
| REST stability | 3.019522 |
| Raw retained stability | 3.161999 |
| Reciprocal-only stability | 1.652996 |
| Exponential-only stability | 5.784956 |
| Exponential-then-reciprocal stability | 3.019522 |
| Mean condition proxy | 1.086070 |
| Min spectral gap | 0.043981 |
| Mean basis motion | 0.312272 |
| Reciprocal clip rate | 0.000000 |
| Exponential clip rate | 0.000000 |

## Quantitative success thresholds

| Threshold | Pass? | Notes |
| --- | --- | --- |
| REST stability within 10% of best ablation on at least 2 of 3 primary drift families | FAIL | threshold_1 |
| There exists a beta regime with mean condition proxy < 2.0 and REST stability < 3.5 on rotating anisotropic Gaussian | PASS | threshold_2 |
| Failure-mode probe documents at least one regime where REST underperforms reciprocal-only | PASS | threshold_3 |
| REST places at least second-best on one controlled downstream benchmark family | PASS | threshold_4 |

## Beta sweep (stability-vs-beta mandate)

| beta | REST stability | Mean condition proxy | Mean spectral gap |
| ---: | ---: | ---: | ---: |
| 0.0 | 1.833135 | 2.336997 | 1.240988 |
| 0.2 | 2.143306 | 2.218589 | 1.240988 |
| 0.4 | 2.509074 | 2.106771 | 1.240988 |
| 0.8 | 3.451367 | 1.901337 | 1.240988 |
| 1.2 | 4.770986 | 1.717801 | 1.240988 |

## Controlled downstream tasks

### Change-point sensitivity

| Representation | Contrast score |
| --- | ---: |
| rest | 0.757039 |
| raw | 0.607050 |
| reciprocal_only | 0.883912 |
| exponential_only | 0.535767 |
| exp_then_reciprocal | 0.757039 |

### Regime clustering separability

| Representation | Fisher ratio |
| --- | ---: |
| rest | 0.057461 |
| raw | 0.044285 |
| reciprocal_only | 0.102778 |
| exponential_only | 0.022381 |
| exp_then_reciprocal | 0.057461 |

### Short-horizon forecasting proxy

| Representation | One-step MSE |
| --- | ---: |
| rest | 5.034453 |
| raw | 4.951410 |
| reciprocal_only | 1.657859 |
| exponential_only | 16.015731 |

## Go / Refine / Pivot rubric

| Exit question | Current answer | Judgment |
| --- | --- | --- |
| Where does REST help? | It remains competitive on some drift families and is computationally stable enough to run richer evaluations. | Mixed-positive |
| Where does REST fail? | The failure probe documents regimes where reciprocal-only behavior can be more stable. | Clear limitation |
| Which parts matter? | Reciprocal and exponential weighting matter; reversed order is algebraically identical in the current retained-coordinate diagonal form. | Important refinement signal |
| How tightly do experiments match theory regime? | Covariance PSD, clipping, and spectral-gap diagnostics are tracked explicitly, but not all experiments remain in uniformly favorable gap regimes. | Partial alignment |
| Scale up or revise first? | In the current retained-coordinate diagonal formulation, reciprocal and exponential weighting commute, so the ordering hypothesis is not empirically testable as a distinct source of benefit. The method still shows viability, but the novelty claim should be reframed or the architecture refined. | REFINE |

## Decision
**Recommended action: REFINE**

In the current retained-coordinate diagonal formulation, reciprocal and exponential weighting commute, so the ordering hypothesis is not empirically testable as a distinct source of benefit. The method still shows viability, but the novelty claim should be reframed or the architecture refined.

## Figure outputs
- `experiments/results/figures/stability_vs_beta.svg`
- `experiments/results/figures/condition_proxy_heatmap.svg`
- `experiments/results/figures/example_embedding_trajectories.svg`
